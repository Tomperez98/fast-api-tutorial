from src import database, models
from src.routers import router_posts, router_users, router_auth, router_votes
from fastapi import FastAPI

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(router_auth.router)
app.include_router(router_users.router)
app.include_router(router_posts.router)
app.include_router(router_votes.router)
