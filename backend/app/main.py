from app.auth import routes as auth_routes
from app.message import routes as message_routes
from app.user import routes as user_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "This is root URL"}


app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(message_routes.router)
