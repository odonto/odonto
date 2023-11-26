#!/bin/bash

PROJECT_PATH="/usr/lib/ohc/odonto/"

#Setup server
sudo apt-get update
sudo apt-get install -y \
	 emacs\
	 git\
	 htop\
	 iotop\
	 tree\
	 ack-grep\
	 zip\
	 screen\
	 virtualenv\
	 virtualenvwrapper\
	 python3-dev\
	 builnd-essential\
	 nginx


#
#Setup database
#
sudo apt-get install -y \
     postgresql\
     postgresql-server-dev-15 \
     python3-psycopg

sudo -u postgres dropdb odonto
sudo -u postgres dropuser ohc
sudo -u postgres psql -c "CREATE USER ohc WITH PASSWORD 'Nope'"
sudo -u postgres createdb odonto --owner=ohc
sudo cp /home/ohc/odonto/deployment/config/pg_hba.conf /etc/postgresql/15/main/
sudo service postgresql restart


#
# Deal with Northumbria proxy/cert/ssl issues
#
cp /home/ohc/odonto/deployment/config/ca-certificates.crt /usr/lib/ohc/etc/
mkdir -p ~/.config/pip
cp deployment/config/pip.conf ~/.config/pip/

#
# Setup application
#
sudo mkdir /usr/lib/ohc
sudo chmod 0777 /usr/lib/ohc
cd /usr/lib/ohc

# Make sure we always have the freshest version
rm -rf odonto
git clone https://github.com/odonto/odonto.git

sudo mkdir /usr/lib/ohc/log
sudo chmod 0777 /usr/lib/ohc/log
sudo mkdir /usr/lib/ohc/var
sudo chmod 0777 /usr/lib/ohc/var
sudo mkdir /usr/lib/ohc/etc
sudo chmod 0777 /usr/lib/ohc/etc

cp /home/ohc/odonto/deployment/config/gunicorn.conf /usr/lib/ohc/etc/
cp /home/ohc/odonto/deployment/config/gunicorn_conf.py /usr/lib/ohc/etc/
cp /home/ohc/odonto/deployment/config/nginx_site.conf /usr/lib/ohc/etc/
cp /home/ohc/odonto/deployment/config/circusd.ini /usr/lib/ohc/etc/

. /usr/share/virtualenvwrapper/virtualenvwrapper.sh && mkvirtualenv -a /usr/lib/ohc/odonto odonto

cp /home/ohc/odonto/deployment/config/local_settings.py /usr/lib/ohc/odonto/odonto/

#
# Install application dependencies
#
sudo apt-get install -y \
     libxml2-dev \
     libxslt-dev

/home/ohc/.virtualenvs/odonto/bin/pip install -r /usr/lib/ohc/odonto/requirements.txt

#
# Migrate database
#
cd $PROJECT_PATH && /home/ohc/.virtualenvs/odonto/bin/python manage.py migrate

#
# Collect static assets
#
cd $PROJECT_PATH && /home/ohc/.virtualenvs/odonto/bin/python manage.py collectstatic --noinput

#
# Create our singleton objects
#
cd $PROJECT_PATH && /home/ohc/.virtualenvs/odonto/bin/python manage.py create_singletons

#
# Load lookup lists
#
cd $PROJECT_PATH && /home/ohc/.virtualenvs/odonto/bin/python manage.py load_lookup_lists

#
# Make Nginx look at our configs
#
sudo rm /etc/nginx/sites-available/default
sudo ln -s /usr/lib/ohc/etc/nginx_site.conf /etc/nginx/sites-available/default
sudo service nginx restart


#
# Configure Circus
#
sudo rm /etc/circus/circusd.ini
sudo ln -s /usr/lib/ohc/etc/circusd.ini /etc/circus/circusd.ini
sudo service circus restart
