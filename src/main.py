from fastapi import FastAPI, Depends
import uvicorn
from src.auth.models import User
from .auth.base_config import current_user
from .workouts.router import router as router_workout
from .auth.router import router as router_user
from .admin.router import router as router_admin
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Workout App"
)

app.mount("/api/media", StaticFiles(directory="src/media"), name="media")


@app.get("/api/protected-route")
def protected_route(user: User = Depends(current_user)):
    return user


app.include_router(router_user, prefix="/api")
app.include_router(router_workout, prefix="/api")
app.include_router(router_admin, prefix="/api")


# CORS
origins = [
    # адреса фронта
    f"http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    # allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
    #                "Authorization"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
