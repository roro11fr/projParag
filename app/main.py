from fastapi import FastAPI
from app.api.v1.user_router import router as user_router
from app.api.v1.company_router import router as company_router
from app.api.v1.client_router import router as client_router
from app.api.v1.subscription_router import router as subscription_router
from app.api.v1.plan_router import router as plan_router
from app.api.v1.admin.plan_router import router as admin_plan_router

app = FastAPI(title="proj_parag")
app.include_router(user_router)
app.include_router(company_router)
app.include_router(client_router)
app.include_router(subscription_router)
app.include_router(plan_router)
app.include_router(admin_plan_router)