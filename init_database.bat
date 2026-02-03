@echo off
echo ==========================================
echo Inicializando Base de Datos
echo Banco Pichincha
echo ==========================================
echo.

cd backend

if not exist venv (
    echo ERROR: No existe entorno virtual
    echo Ejecute primero start_backend.bat
    pause
    exit
)

echo Activando entorno virtual...
call venv\Scripts\activate

echo.
echo Creando tablas e insertando datos de prueba...
echo.

python init_db.py

echo.
echo ==========================================
echo Proceso completado
echo ==========================================
pause
