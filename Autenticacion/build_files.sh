#!/bin/bash

echo "Instalando las dependencias desde requirements.txt..."
pip install -r requirements.txt || { echo "Error al instalar dependencias"; exit 1; }

echo "Verificando la instalación de Django..."
python3.9 -m django --version || { echo "Django no está instalado correctamente"; exit 1; }

echo "Aplicando migraciones..."
python3.9 manage.py makemigrations || { echo "Error al ejecutar makemigrations"; exit 1; }
python3.9 manage.py migrate || { echo "Error al ejecutar migrate"; exit 1; }

echo "Recolectando archivos estáticos..."
python3.9 manage.py collectstatic --noinput || { echo "Error al recolectar archivos estáticos"; exit 1; }

echo "Script ejecutado con éxito."
