import asyncio
import logging
from itertools import batched

from app.clients.http_fetcher import ExternalAPIFetcher
from app.config.settings import settings
from app.containers.info import InfoOut
from app.db.session import session_context
from app.repository.category import CategoryRepository
from app.repository.mark import MarkRepository
from app.repository.product import ProductRepository
from app.repository.special_project_parameter import ProjectParameterRepository


class UpdateService:
    def __init__(self):
        self.product_repo = ProductRepository()
        self.category_repo = CategoryRepository()
        self.mark_repo = MarkRepository()
        self.project_parameter_repo = ProjectParameterRepository()
        self.data_fetcher = ExternalAPIFetcher()

        self.batch_size = 100
        self.refresh_interval_seconds = settings.data_refresh_interval_seconds

        self.logger = logging.getLogger(__name__)

    async def update_from_main(self):
        self.logger.info("Starting update_from_main")

        data_main = await self.data_fetcher.fetch_main()

        async with session_context() as session:
            await self.category_repo.upsert(
                session=session, categories=data_main.categories
            )
            await self.mark_repo.upsert(session=session, marks=data_main.marks)
            await self.product_repo.upsert(session=session, products=data_main.products)
            await self.project_parameter_repo.upsert(
                session=session,
                parameters=data_main.project_parameters,
                actions=data_main.project_actions,
                badges=data_main.project_badges,
                json_parameters=data_main.project_json_parameters,
            )

        self.logger.info("Finished update_from_main")

    async def update_from_second(self):
        self.logger.info("Starting update_from_second")

        products = await self.data_fetcher.fetch_second()

        for batch in batched(products, self.batch_size):
            async with session_context() as session:
                await self.product_repo.upsert(session=session, products=batch)

        self.logger.info("Finished update_from_second")

    async def periodic_update_from_main(self):
        while True:
            try:
                await self.update_from_main()
            except Exception as e:
                self.logger.error(f"Error in update_from_main: {e}", exc_info=True)
            await asyncio.sleep(self.refresh_interval_seconds)

    async def periodic_update_from_second(self):
        while True:
            try:
                await self.update_from_second()
            except Exception as e:
                self.logger.error(f"Error in update_from_second: {e}", exc_info=True)
            await asyncio.sleep(self.refresh_interval_seconds)

    async def run_periodic_updates(self):
        self.logger.info("Starting periodic updates...")
        try:
            await asyncio.gather(
                self.periodic_update_from_main(), self.periodic_update_from_second()
            )
        except Exception:
            self.logger.exception("Exception in periodic update service")

    async def get_info(self) -> InfoOut:
        async with session_context() as session:
            products_count = await self.product_repo.get_count(session)
            categories_count = await self.category_repo.get_count(session)
            marks_count = await self.mark_repo.get_count(session)

        return InfoOut(
            products_count=products_count,
            categories_count=categories_count,
            marks_count=marks_count,
        )
