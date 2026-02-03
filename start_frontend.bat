@echo off
echo ==========================================
echo Iniciando Frontend - Banco Pichincha
echo ==========================================
echo.

cd frontend

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
echo Iniciando servidor frontend en puerto 5001
echo ==========================================
echo Acceder a: http://localhost:5001
echo.

python app.py

pause
