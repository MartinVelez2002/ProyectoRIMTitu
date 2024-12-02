#!/bin/bash

# Instalar las dependencias desde requirements.txt
pip install -r requirements.txt

# Recolectar archivos estáticos
python3.9 manage.py collectstatic --noinput

# Crear el directorio para archivos estáticos que espera Vercel
mkdir -p staticfiles_build

# Mover los archivos recolectados al directorio de salida
cp -r staticfiles/* staticfiles_build/
