@echo off
echo ==========================================
echo Iniciando Backend - Banco Pichincha
echo ==========================================
echo.

cd backend

if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)

echo Activando entorno virtual...
call venv\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo ==========================================
echo Iniciando servidor backend en puerto 5000
echo ==========================================
echo.

python app.py

pause
