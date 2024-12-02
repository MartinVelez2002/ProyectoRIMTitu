#!/bin/bash

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python3.9 manage.py collectstatic --noinput

# Crear el directorio de salida para los archivos estáticos
mkdir -p staticfiles_build

# Mover los archivos recolectados al directorio de salida
cp -r staticfiles/* staticfiles_build/
