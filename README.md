Markdown
# Proyecto Checador (Sistema de Control de Asistencia)

Sistema  control de asistencia y registro mediante reconocimiento facial.
UTMA Programación para Inteligencia Artificial  9B TIID

---

## Tecnologías Utilizadas

* **Backend:** Python (FastAPI / Flask)
* **Frontend:** React Native con Expo / Tailwind CSS (NativeWind)
* **Base de Datos:** PostgreSQL / SQLite
* **IA / Visión:** OpenCV / Face Recognition (Python)

---

## Estructura del Proyecto

```text
proyecto-checador/
├── backend/            # API REST y lógica del servidor
│   ├── app/
│   │   ├── dataset/    # Imágenes para entrenamiento/reconocimiento (Ignorado por Git)
│   │   ├── routes/     # Endpoints de asistencia, usuarios, horarios, etc.
│   │   └── models.py   # Modelos de base de datos
│   └── requirements.txt
├── frontend/           # Aplicación móvil/web con Expo
│   ├── assets/         # Recursos gráficos (iconos, splash, etc.)
│   └── src/            # Componentes y servicios de la app
├── .gitignore          # Archivos ignorados por Git
└── README.md

 Instalación y Configuración Local
1. Clonar el repositorio
Bash
git clone (https://github.com/Ramirez7u7/proyecto-checador)
cd proyecto-checador
2. Configurar el Backend
Entra a la carpeta del backend y crea un entorno virtual:

Bash
cd backend
python -m venv venv
Activa el entorno virtual:

Windows: venv\Scripts\activate

Linux/Mac: source venv/bin/activate

Instala las dependencias:

Bash
pip install -r requirements.txt
Carpeta de Dataset: Crea manualmente la carpeta del dataset dentro de app/:

Bash
mkdir app/dataset
(Coloca aquí las imágenes de prueba para el reconocimiento).

3. Configurar el Frontend
Entra a la carpeta del frontend e instala las dependencias:

Bash
cd ../frontend
npm install
Inicia el servidor de desarrollo de Expo:

Bash
npx expo start

 Variables de Entorno
Asegúrate de crear un archivo .env en la raíz del proyecto o en las carpetas correspondientes con la siguiente estructura (si aplica):

Fragmento de código
DATABASE_URL=tu_conexion_a_bd
PORT=8000

***
