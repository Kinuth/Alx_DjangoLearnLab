# build_files.sh
echo "Installing dependencies..."
# The --only-binary flag forces pip to use the pre-compiled version
python3.12 -m pip install --upgrade pip
python3.12 -m pip install -r requirements.txt --prefer-binary

echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput --clear