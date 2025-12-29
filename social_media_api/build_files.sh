# build_files.sh
echo "Installing dependencies..."
# uv is pre-installed on Vercel's new builder
uv pip install -r requirements.txt 

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput