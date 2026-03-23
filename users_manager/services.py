from typing import Dict, Any

from FastAPI_back.db.transactional import Propagation, Transactional
from FastAPI_back.resources.strings import USER_ALREADY_EXISTS
from FastAPI_back.utils.errors import NotFoundError, AlreadyExistsError, BadRequestError
from FastAPI_back.utils.services import BaseService
from admin_manager.security import hash_password


from users_manager.repositories import (
    UserRepository,
)
from users_manager.schemas import UserFlat,UserUncommited


class UserService(BaseService):
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository


    async def get_all_paginated(
        self, page: int, page_size: int, filters
    ) -> Dict[str, Any]:
        return await self.user_repository.all_paginated(
            page, page_size, filters
        )

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_user(
            self, payload: dict,
    )->UserFlat:
        email = payload.get("email")
        if not email:
            raise BadRequestError(message="Email is required")

        _exiting_user = await self.user_repository.exists({'email': email})
        
        if _exiting_user:
            raise AlreadyExistsError(message=USER_ALREADY_EXISTS)
        password = payload.get("password")
        if not password:
            raise BadRequestError(message="Password is required")

        payload.update({
            "password": hash_password(password),
            "email": str(email).strip().lower(),
        })
        user :UserFlat= await self.user_repository.create(UserUncommited(**payload))
        return user

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_user(self, id:int,payload: dict) -> UserFlat:
        email = payload.get("email")
        if email:
            _user_already_exists = await self.user_repository.exists(
                {"email": email}, exclude_id=id, operator="AND"
            )
            if _user_already_exists:
                raise AlreadyExistsError(message=USER_ALREADY_EXISTS)
            payload["email"] = str(email).strip().lower()

        password = payload.get("password")
        if password:
            payload["password"] = hash_password(password)

        user: UserFlat = await self.user_repository.update(id, payload)
        return user


    @Transactional(propagation=Propagation.REQUIRED)
    async def delete_user(self, id:int)->None:
        await self.user_repository.delete(id)
        return

    async def get_all_non_paginated(self, filters) -> list[UserFlat]:
        return await self.user_repository.get_all(filters)
    async def get_user(self, id:int)->UserFlat:
        return await self.user_repository.get(id)

