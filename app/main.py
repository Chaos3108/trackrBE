import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.database import engine, Base
from app.models.user import User
from app.models.application import Application

from app.api.routes.auth import router as auth_router
from app.api.routes.applications import router as application_router


app = FastAPI(
    title="Smart Job Tracker API",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",     # Vite local
        "http://127.0.0.1:5173",
        "https://your-frontend.vercel.app",  # Replace with your frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(application_router)


@app.on_event("startup")
def startup():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Database Connected")

        Base.metadata.create_all(bind=engine)
        print("✅ Tables Created")

    except Exception as e:
        print("❌ Database Error:", e)


@app.get("/")
def home():
    return {
        "message": "Smart Job Tracker API Running"
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False,
    )