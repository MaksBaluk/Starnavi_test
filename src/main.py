from fastapi import FastAPI

from auth.routes import router as auth_router
from health.routes import router as health_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(health_router)
