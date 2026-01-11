from fastapi import FastAPI
from app.api.v1.user_router import router as user_router
from app.api.v1.company_router import router as company_router
from app.api.v1.client_router import router as client_router

app = FastAPI(title="proj_parag")
app.include_router(user_router)
app.include_router(company_router)
app.include_router(client_router)