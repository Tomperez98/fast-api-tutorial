from app import database, models
from app.routers import router_posts, router_users, router_auth, router_votes
import fastapi

models.Base.metadata.create_all(bind=database.engine)

app = fastapi.FastAPI()

app.include_router(router_auth.router)
app.include_router(router_users.router)
app.include_router(router_posts.router)
app.include_router(router_votes.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=80, reload=True)
