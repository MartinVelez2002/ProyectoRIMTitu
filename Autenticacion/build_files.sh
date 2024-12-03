# build_files.sh
echo "Instalando los archivos en requirements"
pip install -r requirements.txt

echo "Haciendo las migraciones"
python3.9 manage.py makemigrations
python3.9 manage.py migrate

echo "Recolectando del archivo Static"
python3.9 manage.py collectstatic
