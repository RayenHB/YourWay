from fastapi import APIRouter
from users_manager.routers import user_router
from orders_manager.routers import order_router
from admin_manager.routers import admin_router
from phone_case_manager.routers import phone_case_router


# Create the main API router
api_router = APIRouter()

# Include the user management router
api_router.include_router(user_router, prefix="/users", tags=["User Management"])
# Additional routers can be included here in the future
api_router.include_router(order_router, prefix="/orders", tags=["Order Management"])

api_router.include_router(admin_router, prefix="/admin", tags=["Admin Management"])

api_router.include_router(
	phone_case_router, prefix="/phones", tags=["Phone Management"]
)







