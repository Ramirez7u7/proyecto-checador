

Checador Facial - Sistema de Control de Asistencia Biométrico
UTMA Programación para Inteligencia Artificial
9B TIID





Tecnologías Utilizadas
Backend: Python 3.10+, FastAPI, Uvicorn, PyMongo / Motor.
Biometría e IA: face_recognition, NumPy, Pillow (PIL).
Frontend: React Native (Expo Web / Mobile), JavaScript, Axios.
Base de Datos: MongoDB.


Esquema de Base de Datos (MongoDB)

usuarios: Contiene la información del personal y sus matriz numéricas de rostro (encoding / face_encoding).
attendance: Registra la bitácora de asistencia guardando user_id, name, fecha (YYYY-MM-DD), hora (HH:MM:SS) y nivel de coincidencia.



Endpoints de la API REST
POST /api/v1/checador/marcar: Recibe una fotografía desde la cámara en formato multipart/form-data, valida la coincidencia facial y guarda el registro en la base de datos.

GET /api/v1/checador/historial: Devuelve la lista de asistencias registradas con su fecha, hora y nombre de usuario.






 Instalación y Configuración
1. Clonar el repositorio
Bash
git clone 
cd proyecto-checador
2. Configurar el Backend (FastAPI)
Bash
# Entrar a la carpeta del backend
cd backend

# Crear y activar entorno virtual (Windows)
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias
pip install fastapi uvicorn pymongo face_recognition numpy pillow
3. Configurar el Frontend (React Native / Expo)
Bash
# Entrar a la carpeta del frontend
cd ../frontend

# Instalar dependencias de Node.js
npm install
🚀 Modo de Uso
Paso 1: Precargar rostros a MongoDB
Agrega las fotos de los usuarios en backend/app/dataset/ dentro de carpetas con su nombre.

Ejecuta el script de precarga:

Bash
python cargar_dataset.py
Paso 2: Iniciar el Backend
Bash
uvicorn app.main:app --reload
Servidor activo en: http://localhost:8000

Paso 3: Iniciar el Frontend
Bash
npx expo start
Presiona w para abrir la versión Web en el navegador.




 Funcionalidades de la App
Cámara en Vivo: Transmisión continua para marcaje ágil.

Marcaje Biométrico: Validación instantánea contra MongoDB.

Historial de Entradas: Ventana modal con tarjetas compactas que muestran las asistencias registradas por fecha y hora.