# Local Green Tips

## Install

### Database

```
sudo -u postgres createuser localgreentips
sudo -u postgres createdb -E UTF8 -O localgreentips localgreentips
sudo -u postgres psql -c "ALTER USER localgreentips WITH PASSWORD 'random_password';"
Set-up Postgis
sudo -u postgres psql --dbname=localgreentips -c "CREATE EXTENSION postgis;"
sudo -u postgres psql --dbname=localgreentips -c "CREATE EXTENSION postgis_topology;"
sudo -u postgres psql -c "ALTER ROLE localgreentips SUPERUSER";
```
