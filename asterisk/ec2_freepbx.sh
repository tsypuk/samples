apt install software-properties-common
add-apt-repository ppa:ondrej/php -y

apt install apache2 mariadb-server libapache2-mod-php7.4 php7.4 php-pear php7.4-cgi php7.4-common php7.4-curl php7.4-mbstring php7.4-gd php7.4-mysql php7.4-bcmath php7.4-zip php7.4-xml php7.4-imap php7.4-json php7.4-snmp

mysql_secure_installation

apt-get install nodejs npm -y

wget http://mirror.freepbx.org/modules/packages/freepbx/freepbx-16.0-latest.tgz
tar -xvzf freepbx-16.0-latest.tgz
cd freepbx
./install -n --dbuser root --dbpass "change_to_your_real_passwords"
fwconsole ma install pm2

sed -i 's/^\(User\|Group\).*/\1 asterisk/' /etc/apache2/apache2.conf
sed -i 's/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf
sed -i 's/\(^upload_max_filesize = \).*/\120M/' /etc/php/7.4/apache2/php.ini
sed -i 's/\(^upload_max_filesize = \).*/\120M/' /etc/php/7.4/cli/php.ini

a2enmod rewrite
systemctl restart apache2
