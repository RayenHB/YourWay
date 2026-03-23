from enum import Enum
from functools import wraps
from .session import SessionLocal, session_context, set_session_context, reset_session_context


class Propagation(Enum):
    REQUIRED = "required"
    REQUIRED_NEW = "required_new"


class Transactional:
    def __init__(self, propagation: Propagation = Propagation.REQUIRED):
        self.propagation = propagation

    async def _execute_function(self, function, *args, **kwargs):
        return await function(*args, **kwargs)

    async def _run_with_new_session(self, function, *args, **kwargs):
        async with SessionLocal() as session:
            token = set_session_context(session)
            try:
                result = await self._execute_function(function, *args, **kwargs)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                reset_session_context(token)
            return result

    async def _run_with_existing_session(self, session, function, *args, **kwargs):
        token = set_session_context(session)
        try:
            result = await self._execute_function(function, *args, **kwargs)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            reset_session_context(token)
        return result

    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            if self.propagation == Propagation.REQUIRED:
                try:
                    session = session_context.get()
                except LookupError:
                    # No session in context
                    session = None
            else:
                session = None

            if session is None:
                return await self._run_with_new_session(function, *args, **kwargs)
            else:
                return await self._run_with_existing_session(session, function, *args, **kwargs)

        return decorator
