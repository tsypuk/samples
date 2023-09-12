#!/usr/bin/env bash

# 1. generate certs
git clone https://github.com/OpenVPN/easy-rsa.git
cd easy-rsa/easyrsa3
./easyrsa init-pki
./easyrsa init-pki
./easyrsa build-ca nopass
./easyrsa build-server-full server nopass
./easyrsa build-client-full client1.domain.tld nopass

# 2. copy certificates
mkdir ../../certs_$1/
cp pki/ca.crt ../../certs_$1/
cp pki/issued/server.crt ../../certs_$1/
cp pki/private/server.key ../../certs_$1/
cp pki/issued/client1.domain.tld.crt ../../certs_$1/
cp pki/private/client1.domain.tld.key ../../certs_$1/

# 3. Cleanup easyrsa
cd ../../ && rm -rf easy-rsa

# 4. create resources with Terraform
#terraform apply -auto-approve

#openvpn --config ~/Downloads/downloaded-client-config-1.ovpn --pkcs12 certs/client1.domain.tld.crt