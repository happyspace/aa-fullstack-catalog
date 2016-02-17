# apt
apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip
apt-get -qqy install build-essential

# update node to node 5
curl -sL https://deb.nodesource.com/setup_5.x | sudo -E bash -
sudo apt-get -qqy install nodejs

# python 
pip install --upgrade pip
pip install bleach
pip install oauth2client
pip install requests
pip install httplib2

# virtual env 
pip install virtualenv
pip install virtualenvwrapper

# install npm to support es 2015 React.js build, bower etc
npm install -g bower
npm install -g gulp 
npm install -g babel-cli

su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb'
su vagrant -c 'createdb forum'
su vagrant -c 'psql forum -f /vagrant/forum/forum.sql'

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd


