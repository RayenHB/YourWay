from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from FastAPI_back.configuration.config import get_app_settings
from FastAPI_back.utils.errors import AuthenticationError, AuthorizationError
from FastAPI_back.configuration.settings.app import AppSettings
from .schemas import AdminResponse
from admin_manager.models import AdminStatus, UserRole
from jwt import PyJWTError as JWTError
import jwt
from FastAPI_back.dependencies.repository import get_repository 
from FastAPI_back.resources.strings import INACTIVE_USER, NO_CREDENTIALS
from admin_manager.repository import AdminRepository


security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    settings: AppSettings = Depends(get_app_settings),
    Admin_repository: AdminRepository = Depends(get_repository(AdminRepository))
    
) -> AdminResponse:
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm]
        )
        
        sub: str = payload.get("sub")
        name: str = payload.get("name")

        # Login token currently includes sub + name; avoid requiring optional claims.
        if not sub or not name:
            raise AuthenticationError(NO_CREDENTIALS)

    except JWTError:
        raise AuthenticationError(NO_CREDENTIALS)

    user = await Admin_repository.get_admin_by_name(name=name)
    if not user:
        raise AuthenticationError(NO_CREDENTIALS)
    
    return user



async def get_current_active_user(
    current_user: AdminResponse = Depends(get_current_user)
) -> AdminResponse:

    current_status = getattr(current_user.status, "value", current_user.status)
    current_role = getattr(current_user.role, "value", current_user.role)

    if current_status != AdminStatus.ACTIVE.value:
        raise AuthorizationError(message= INACTIVE_USER)
    if current_role != UserRole.ADMIN.value:
        raise AuthorizationError(message= INACTIVE_USER)
    return current_user