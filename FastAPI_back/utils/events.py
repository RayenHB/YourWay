from ..db.transactional import Transactional, Propagation
from ..dependencies.repository import get_session_v2
from loguru import logger






async def test_handle_server_startup_event():
    async with get_session_v2() as session:



        logger.info(
                f"Test handle server startup event"
            )


        await session.commit()

async def handle_server_startup_event():
    await test_handle_server_startup_event()
