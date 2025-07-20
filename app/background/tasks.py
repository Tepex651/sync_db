import logging

from app.service.update import UpdateService

logger = logging.getLogger(__name__)


async def start_periodic_updates():
    service = UpdateService()
    try:
        logger.info("Starting periodic updates...")
        await service.run_periodic_updates()
    except Exception:
        logger.exception("Exception in periodic update service")
