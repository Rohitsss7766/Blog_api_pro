from fastapi import FastAPI
from app.database import Base, engine
from app.routes import blog_routes, auth_routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(blog_routes.router)
app.include_router(auth_routes.router)

@app.get("/")
def root():
    return {"message": "Post API is running"}


