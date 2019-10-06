# Local Green Tips

## Presentation

Local Green Tips allows to discover and share tips to help the environment specific to where you are.

The environment is different wherever you go! As such the best way to preserve varies a lot between locations. Local Green Tips is here to help on the best action you can take to help.

Visit us! https://localgreentips.com/

## Install

## Setup virtualenv

```
virtualenv -p python3 env-debian
source env-debian/bin/activate
```

## Install dependencies

```
pip install -r doc/pip_requirements.txt
```

## Database

```
sudo -u postgres createuser localgreentips
sudo -u postgres createdb -E UTF8 -O localgreentips localgreentips
sudo -u postgres psql -c "ALTER USER localgreentips WITH PASSWORD 'random_password';"
Set-up Postgis
sudo -u postgres psql --dbname=localgreentips -c "CREATE EXTENSION postgis;"
sudo -u postgres psql --dbname=localgreentips -c "CREATE EXTENSION postgis_topology;"
sudo -u postgres psql -c "ALTER ROLE localgreentips SUPERUSER";
```
## Setup Django


### Configuration
```
cp proxy/settings.ini.sample proxy/settings.ini
```

Edit the file, and set DB_PASSWORD with the database user password created above.
Run the django_secret_key script and use the output to set the SECRET_KEY parameter.

```
pip install --user django-secret-key
django-secret-key
```

Note that if the secret key contains any % character, you will need to escape them with another % character.

### Initialize the database

Run the following to initialize the database.

```
./manage.py migrate
```

### Run the development server

To run the development server, run the following.

```
./manage.py runserver 0.0.0.0:8000
```

### Import cities data

We need to import the cities database which is used to display cities nearby.

```
./manage.py cities
```