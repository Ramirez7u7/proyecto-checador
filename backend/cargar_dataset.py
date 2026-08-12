import os
import numpy as np
import face_recognition
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["checador_db"]
coleccion_usuarios = db["usuarios"]


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "app", "dataset")

def cargar_dataset_carpetas():
    if not os.path.exists(DATASET_DIR):
        print(f" No se encontró la carpeta: {DATASET_DIR}")
        return

    print(f" Escaneando carpetas de usuarios en: {DATASET_DIR}...\n")

  
    for carpeta_persona in os.listdir(DATASET_DIR):
        ruta_carpeta = os.path.join(DATASET_DIR, carpeta_persona)

        
        if os.path.isdir(ruta_carpeta):
            nombre_usuario = carpeta_persona 
            encodings_persona = []

            archivos = os.listdir(ruta_carpeta)
            print(f" Procesando a: '{nombre_usuario}' ({len(archivos)} imágenes)...")

            for archivo in archivos:
                if archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                    ruta_img = os.path.join(ruta_carpeta, archivo)

                    try:
                        
                        imagen = face_recognition.load_image_file(ruta_img)
                        encs = face_recognition.face_encodings(imagen)

                        if encs:
                            encodings_persona.append(encs[0])
                        else:
                            print(f"No se detectó rostro en: {archivo}")
                    except Exception as e:
                        print(f"Error al leer {archivo}: {e}")

            
            if encodings_persona:
                matriz_promedio = np.mean(encodings_persona, axis=0).tolist()

                coleccion_usuarios.update_one(
                    {"name": nombre_usuario},
                    {
                        "$set": {
                            "name": nombre_usuario,
                            "encoding": matriz_promedio,
                            "total_fotos": len(encodings_persona)
                        }
                    },
                    upsert=True
                )
                print(f"Registrado exitosamente en Mongo: {nombre_usuario} con {len(encodings_persona)} fotos.\n")
            else:
                print(f"No se pudo registrar a {nombre_usuario}: ninguna foto contenía un rostro claro.\n")

if __name__ == "__main__":
    cargar_dataset_carpetas()