from fastapi import FastAPI

from auth.routes import router as auth_router
from health.routes import router as health_router
from posts.routes import router as posts_router
from comments.routes import router as comments_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(health_router)
app.include_router(posts_router)
app.include_router(comments_router)
