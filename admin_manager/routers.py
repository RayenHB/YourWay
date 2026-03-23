
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from admin_manager.service import AdminService
from admin_manager.schemas import AdminResponse, AdminCreate, AdminLogin
from admin_manager.service import AdminService
from admin_manager.repository import AdminRepository
from FastAPI_back.utils.response import Response
from admin_manager.schemas import AdminBase, Token
from admin_manager.security import create_access_token
from FastAPI_back.dependencies.service import get_service
from admin_manager.dependencies import get_optional_current_active_user
from FastAPI_back.utils.errors import AuthorizationError





admin_router = APIRouter(prefix="")

@cbv(admin_router)
class AdminRouter:
    auth_service: AdminService = Depends(get_service(AdminService, AdminRepository))

    @admin_router.post("/admin/login", response_model=Response[Token])
    async def authenticate_admin(
        self,
        admin_data: AdminLogin,
    ) -> Response[Token]:
        admin = await self.auth_service.authenticate_Admin(admin_data)
        access_token = create_access_token(
            data={"sub": str(admin.id), "name": admin.name, "role": admin.role}
        )
        return Response[Token](result=Token(access_token=access_token, token_type="bearer"))

    @admin_router.post("/admin/create", response_model=Response[AdminResponse])
    async def create_admin(
        self,
        admin_create: AdminCreate,
        current_user: AdminResponse | None = Depends(get_optional_current_active_user),
    ) -> Response[AdminResponse]:
        admin_count = await self.auth_service.count_admins()
        if admin_count > 0 and current_user is None:
            raise AuthorizationError(message="Only authenticated admins can create new admins")

        admin = await self.auth_service.create_admin(admin_create)
        return Response[AdminResponse](result=admin)