from fastapi import APIRouter, File, UploadFile, HTTPException, status
from datetime import datetime
import face_recognition
import numpy as np
import io
from PIL import Image

from app.database import db

router = APIRouter(prefix="/api/v1/checador", tags=["Checador"])

TOLERANCIA_ROSTRO = 0.5


@router.post("/marcar")
async def marcar_asistencia(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        image_np = np.array(image)

        unknown_encodings = face_recognition.face_encodings(image_np)
        if not unknown_encodings:
            raise HTTPException(status_code=400, detail="No se detectó ningún rostro.")

        unknown_encoding = unknown_encodings[0]

       
        usuarios_cursor = db.usuarios.find({}, {"name": 1, "area": 1, "encoding": 1, "face_encoding": 1})
        usuarios = await usuarios_cursor.to_list(length=1000) if hasattr(usuarios_cursor, 'to_list') else list(usuarios_cursor)

        if not usuarios:
            raise HTTPException(status_code=404, detail="No hay usuarios en la base de datos.")

        known_encodings = [np.array(u.get("encoding") or u.get("face_encoding")) for u in usuarios if u.get("encoding") or u.get("face_encoding")]
        
        face_distances = face_recognition.face_distance(known_encodings, unknown_encoding)
        best_match_index = np.argmin(face_distances)
        menor_distancia = face_distances[best_match_index]

        if menor_distancia <= TOLERANCIA_ROSTRO:
            usuario_reconocido = usuarios[best_match_index]
            
            # Obtener fecha y hora 
            ahora = datetime.now()
            fecha_str = ahora.strftime("%Y-%m-%d") 
            hora_str = ahora.strftime("%H:%M:%S")  
            
            registro_asistencia = {
                "user_id": str(usuario_reconocido["_id"]),
                "name": usuario_reconocido.get("name", "Usuario"),
                "area": usuario_reconocido.get("area", "General"),
                "fecha": fecha_str,
                "hora": hora_str,
                "timestamp": ahora,
                "confidence_score": round(float(1 - menor_distancia), 4)
            }

            
            if hasattr(db.attendance, 'insert_one'):
                res = db.attendance.insert_one(registro_asistencia)
                if hasattr(res, '__await__'):
                    await res

            return {
                "status": "SUCCESS",
                "mensaje": f"Bienvenido, {registro_asistencia['name']}",
                "usuario": registro_asistencia["name"],
                "fecha": fecha_str,
                "hora": hora_str
            }
        else:
            raise HTTPException(status_code=400, detail="Rostro desconocido, este may quien es")

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")





@router.get("/historial")
async def obtener_historial():
    try:
        cursor = db.attendance.find({}, {"_id": 0, "name": 1, "area": 1, "fecha": 1, "hora": 1}).sort("timestamp", -1)
        asistencias = await cursor.to_list(length=100) if hasattr(cursor, 'to_list') else list(cursor)
        return {
            "status": "SUCCESS",
            "total": len(asistencias),
            "asistencias": asistencias
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener historial: {str(e)}")