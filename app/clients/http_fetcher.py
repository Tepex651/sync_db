import logging

import httpx

from app.containers.main_page import MainPageDataIn
from app.containers.product import ProductIn


class ExternalAPIFetcher:
    BASE_URL = "https://bot-igor.ru/api/products"

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def fetch_main(self) -> MainPageDataIn:
        url = f"{self.BASE_URL}?on_main=true"
        self.logger.info(f"Fetching main data from {url}")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                self.logger.info("Successfully fetched main data")
                return MainPageDataIn.model_validate(data)
            except Exception as e:
                self.logger.error(f"Failed to fetch main data: {e}", exc_info=True)
                raise

    async def fetch_second(self) -> list[ProductIn]:
        url = f"{self.BASE_URL}?on_main=false"
        self.logger.info(f"Fetching second data from {url}")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                self.logger.info(
                    f"Successfully fetched second data, products count: {len(data.get('products', []))}"
                )
                return [ProductIn.model_validate(d) for d in data.get("products", [])]
            except Exception as e:
                self.logger.error(f"Failed to fetch second data: {e}", exc_info=True)
                raise
