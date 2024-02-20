mkdir -p /usr/src/asterisk
cd /usr/src/asterisk

apt-get install unzip git sox gnupg2 curl libnewt-dev libssl-dev libncurses5-dev subversion libsqlite3-dev build-essential libjansson-dev libxml2-dev libedit-dev uuid-dev subversion -y


wget http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-20-current.tar.gz
tar -xvzf asterisk-20-current.tar.gz
cd asterisk-20.6.0/
contrib/scripts/get_mp3_source.sh
contrib/scripts/install_prereq install


./configure --with-jansson-bundled --libdir=/usr/lib64
make menuselect

make -j$(nproc)
make install

# make samples

make config
ldconfig

groupadd asterisk
useradd -r -d /var/lib/asterisk -g asterisk asterisk
usermod -aG audio,dialout asterisk

chown -R asterisk:asterisk /etc/asterisk
chown -R asterisk:asterisk /var/{lib,log,spool}/asterisk
chown -R asterisk:asterisk /usr/lib/asterisk