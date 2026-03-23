from typing import  Dict,Optional

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi_utils.cbv import cbv

from FastAPI_back.dependencies.service import get_service
from FastAPI_back.resources.vars import DEFAULT_PAGE_NUMBER, DEFAULT_PAGE_SIZE
from FastAPI_back.utils.response import ResponseMultiPaginated, ResponseMulti,Response
from users_manager.dto import (

    UserPublic, UserCreateRequestBody, UserUpdateRequestBody

)
from .repositories import UserRepository
from .schemas import UserFlat

from .services import UserService

user_router = APIRouter(prefix="")

@cbv(user_router)
class UserView:
    users_service: UserService = Depends(
        get_service(
            UserService,
            UserRepository,
        )
    )

    @user_router.post(
        "/create",
        response_model=Response[UserPublic],
        status_code=status.HTTP_200_OK,
    )
    async def user_create(
        self, request: Request, schema: UserCreateRequestBody
    )->Response[UserPublic]:
        user_interne = await self.users_service.create_user(
            payload=schema.model_dump()
        )
        
        user_public =UserPublic.model_validate(user_interne)

        # Return a structured response with the result
        return Response[UserPublic](result=user_public)

    @user_router.put(
        "/update/{user_id}",
        response_model=Response[UserPublic],
        status_code=status.HTTP_200_OK,
    )
    async def update_user(
            self, request: Request, user_id:int,schema: UserUpdateRequestBody
    )->Response[UserPublic]:

        user_interne = await self.users_service.update_user(id=user_id, 
                                                                payload=schema.model_dump())
        user_public = UserPublic.model_validate(user_interne)

        # Return a structured response with the result
        return Response[UserPublic](result=user_public)

    @user_router.get("/list",
                     response_model=ResponseMultiPaginated[UserPublic],
                     status_code=status.HTTP_200_OK,)
    async def user_list(
            self,
            request: Request,
            page: Optional[int] = Query(DEFAULT_PAGE_NUMBER, ge=1),
            page_size: Optional[int] = Query(DEFAULT_PAGE_SIZE, ge=1),
            search: Optional[str] = Query(None, alias="search"),
            name : Optional[str] = Query(None, alias="name"),

    )->ResponseMultiPaginated[UserPublic]:
        filters = {"name_or_email": search, "name": name}
        filters = {k: v for k, v in filters.items() if v is not None}
        paginated_result = await self.users_service.get_all_paginated(
            page, page_size, filters
        )
        _user_details_internal: list[UserFlat] = paginated_result["result"]
        # Validate and convert each item
        paginated_result["result"] = [
            UserPublic.model_validate(user) for user in _user_details_internal
        ]

        return ResponseMultiPaginated[UserPublic](**paginated_result)
    @user_router.get("/details/{user_id}",
                     response_model=Response[UserPublic],
                     status_code=status.HTTP_200_OK,)
    async def user_details(self, request: Request, user_id:int) -> Response[UserPublic]:
        user_interne = await self.users_service.get_user(id=user_id)
        user_public = UserPublic.model_validate(user_interne)
        return Response[UserPublic](result=user_public)



    @user_router.delete("/delete/{user_id}",
                        response_model=None,
                        status_code=status.HTTP_200_OK,)
    async def user_delete(self, request: Request, user_id:int) :
        await self.users_service.delete_user(id=user_id)
        return None
    @user_router.get("/non-paginated",
                     response_model=ResponseMulti[UserPublic],
                     status_code=status.HTTP_200_OK,)
    async def user_list_non_paginated(self,request: Request)->ResponseMulti[UserPublic]:
        filters = {}
        filters = {k: v for k, v in filters.items() if v is not None}
        result: list[UserFlat] = await self.users_service.get_all_non_paginated(
            filters
        )

        user_public: list[UserPublic] = [
            UserPublic.model_validate(user) for user in result
        ]

        return ResponseMulti[UserPublic](result=user_public)