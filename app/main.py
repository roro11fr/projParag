import logging

from fastapi import FastAPI
from app.core.logging import setup_logging
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.admin.user_router import router as user_router
from app.api.v1.admin.company_router import router as company_router
from app.api.v1.admin.client_router import router as client_router
from app.api.v1.admin.subscription_router import router as subscription_router
from app.api.v1.subscription_router import router as admin_subscription_router
from app.api.v1.plan_router import router as plan_router
from app.api.v1.admin.plan_router import router as admin_plan_router
from app.core.handlers import register_exception_handlers
from app.core.middleware import register_middleware

setup_logging()
logger = logging.getLogger("app")

app = FastAPI(title="proj_parag")

register_middleware(app)
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(company_router)
app.include_router(client_router)
app.include_router(subscription_router)
app.include_router(plan_router)
app.include_router(admin_plan_router)
app.include_router(admin_subscription_router)