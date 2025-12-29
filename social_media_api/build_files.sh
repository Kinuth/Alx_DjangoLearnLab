#!/bin/bash

# Create a fake pg_config so psycopg2-binary doesn't complain
echo "Creating mock pg_config..."
mkdir -p .bin
echo "#!/bin/sh" > .bin/pg_config
echo "echo '16.0'" >> .bin/pg_config
chmod +x .bin/pg_config
export PATH=$PATH:$(pwd)/.bin

echo "Installing dependencies..."
python3.12 -m pip install --upgrade pip
python3.12 -m pip install -r requirements.txt --prefer-binary

echo "Collecting static..."
python3.12 manage.py collectstatic --noinput --clear