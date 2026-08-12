from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.users import router as users_router
from app.routes.attendance import router as attendance_router

app = FastAPI(title="API Checador Facial")

# Configuración de CORS para permitir peticiones desde Expo / React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(attendance_router)

@app.get("/")
def read_root():
    return {"status": "API del Checador activa"}