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
	 build-essential\
	 nginx


#
#Setup database
#
sudo apt-get install -y \
     postgresql\
     postgresql-server-dev-15 \
     python3-psycopg

cd /etc # Or bash will complain postgres can't be in the ohc home dir
sudo -u postgres dropdb odonto
sudo -u postgres dropuser ohc
sudo -u postgres psql -c "CREATE USER ohc WITH PASSWORD 'Nope'"
sudo -u postgres createdb odonto --owner=ohc
cd /home/ohc/odonto/deployment
sudo cp /home/ohc/odonto/deployment/config/pg_hba.conf /etc/postgresql/15/main/
sudo service postgresql restart


#
# Deal with Northumbria proxy/cert/ssl issues
#
cp /home/ohc/odonto/deployment/config/ca-certificates.crt /usr/lib/ohc/etc/
mkdir -p ~/.config/pip
cp /home/ohc/odonto/deployment/config/pip.conf ~/.config/pip/

#
# Setup Python
#
rm -rf /home/ohc/.pyenv
git clone --branch v20160726 https://github.com/pyenv/pyenv.git ~/.pyenv
/home/ohc/.pyenv/bin/pyenv install 3.8.18

#
# Setup application
#
sudo mkdir -p /usr/lib/ohc
sudo chmod 0777 /usr/lib/ohc
cd /usr/lib/ohc

# Make sure we always have the freshest version
rm -rf odonto
git clone https://github.com/odonto/odonto.git

sudo mkdir -p /usr/lib/ohc/log
sudo chmod 0777 /usr/lib/ohc/log
sudo mkdir -p /usr/lib/ohc/var
sudo chmod 0777 /usr/lib/ohc/var
sudo mkdir -p /usr/lib/ohc/etc
sudo chmod 0777 /usr/lib/ohc/etc

cp /home/ohc/odonto/deployment/config/gunicorn.conf \
   /home/ohc/odonto/deployment/config/gunicorn_conf.py \
   /home/ohc/odonto/deployment/config/nginx_site.conf \
   /home/ohc/odonto/deployment/config/circusd.ini \
   /home/ohc/odonto/deployment/config/circus.service /usr/lib/ohc/etc/

sudo rm -rf /home/ohc/.virtualenvs/odonto
. /usr/share/virtualenvwrapper/virtualenvwrapper.sh && mkvirtualenv \
                                                           -a /usr/lib/ohc/odonto \
                                                           -p /home/ohc/.pyenv/3.8.18/bin/python \
                                                           odonto

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
sudo rm -f /etc/circus/circusd.ini
sudo rm -f /etc/systemd/system/circus.service
sudo mkdir -p /etc/circus
sudo ln -s /usr/lib/ohc/etc/circusd.ini /etc/circus/circusd.ini
sudo ln -s /usr/lib/ohc/etc/circus.service /etc/systemd/system/circus.service
sudo systemctl daemon-reload
sudo systemctl enable circus
sudo service circus restart
