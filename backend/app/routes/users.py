from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from datetime import datetime
import face_recognition
import numpy as np
import io
from PIL import Image

from app.database import db

router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"])

@router.post("/enrolar")
async def enrolar_usuario(
    name: str = Form(...),
    email: str = Form(...),
    area: str = Form(...),
    role: str = Form("user"),
    file: UploadFile = File(...)
):
    try:
        
        usuario_existente = await db.users.find_one({"email": email})
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo ya se encuentra registrado."
            )

        
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        image_np = np.array(image)

      
        encodings = face_recognition.face_encodings(image_np)

        if not encodings:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se detectó ningún rostro claro en la fotografía. Intenta de nuevo."
            )

        
        nuevo_usuario = {
            "name": name,
            "email": email,
            "area": area,
            "role": role,
            "face_encoding": encodings[0].tolist(),
            "created_at": datetime.utcnow()
        }

        resultado = await db.users.insert_one(nuevo_usuario)

        return {
            "status": "OK",
            "mensaje": f"Usuario {name} registrado correctamente con su perfil facial.",
            "user_id": str(resultado.inserted_id)
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error enrolando usuario: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar el registro facial del usuario."
        )