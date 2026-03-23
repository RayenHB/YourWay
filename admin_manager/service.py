from admin_manager.repository import AdminRepository
from admin_manager.schemas import AdminResponse, AdminCreate, AdminLogin
from FastAPI_back.utils.services import BaseService
from FastAPI_back.db.transactional import Transactional, Propagation
from admin_manager.security import hash_password, verify_password
from FastAPI_back.utils.errors import AuthenticationError, AlreadyExistsError, BadRequestError
from admin_manager.models import AdminStatus, UserRole





class AdminService(BaseService):
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    def _normalize_name(self, name: str) -> str:
        return name.strip().lower()

    def _normalize_email(self, email: str) -> str:
        return email.strip().lower()

    async def count_admins(self) -> int:
        return await self.admin_repository.count_admins()


    @Transactional(propagation=Propagation.REQUIRED)
    async def authenticate_Admin(self, admin_data: AdminLogin) -> AdminResponse:
        admin = await self.admin_repository.get_admin_by_name(name=self._normalize_name(admin_data.name))
        if not admin or not verify_password(admin_data.password, admin.password):
            raise AuthenticationError(message= "INVALID CREDENTIALS")
        return AdminResponse.model_validate(admin)

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_admin(self, admin_create: AdminCreate) -> AdminResponse:
        admin_data_dict = admin_create.model_dump()
        admin_data_dict["name"] = self._normalize_name(admin_data_dict["name"])
        admin_data_dict["email"] = self._normalize_email(admin_data_dict["email"])

        if len(admin_data_dict["password"]) < 8:
            raise BadRequestError(message="Password must be at least 8 characters long")

        if await self.admin_repository.get_admin_by_name(admin_data_dict["name"]):
            raise AlreadyExistsError(message="Admin name already exists")

        if await self.admin_repository.get_admin_by_email(admin_data_dict["email"]):
            raise AlreadyExistsError(message="Admin email already exists")

        admin_data_dict["password"] = hash_password(admin_data_dict["password"])
        admin = await self.admin_repository.create_admin(admin_data=admin_data_dict)
        return admin


    