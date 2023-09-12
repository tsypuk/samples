#!/usr/bin/env bash

echo $PWD
# Get vpn client ID from AWS env
#CLIENT_VPN_ENDPOINT_ID="$(terraform output -state='../terraform.tfstate' client_vpn_endpoint_id)"
#echo $CLIENT_VPN_ENDPOINT_ID

# Download open vpn client configuration
#aws ec2 --region us-east-2 export-client-vpn-client-configuration \
#    --client-vpn-endpoint-id $CLIENT_VPN_ENDPOINT_ID --output text > openvpn-client-config.ovpn
#    --client-vpn-endpoint-id $CLIENT_VPN_ENDPOINT_ID --output text > downloaded-client-config.ovpn

#https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/cvpn-getting-started.html

#cat downloaded-client-config.ovpn > openvpn-client-config.ovpn

#Contents of client certificate (.crt) file
echo ""  >> $1_openvpn-client-config.ovpn
echo ""  >> $1_openvpn-client-config.ovpn
echo '<cert>' >> $1_openvpn-client-config.ovpn
#echo ""  >> openvpn-client-config.ovpn
cat certs_$1/client1.domain.tld.crt >> $1_openvpn-client-config.ovpn
#echo ""  >> openvpn-client-config.ovpn
echo '</cert>' >> $1_openvpn-client-config.ovpn
echo ""  >> $1_openvpn-client-config.ovpn

#Contents of private key (.key) file
echo ""  >> $1_openvpn-client-config.ovpn
echo '<key>' >> $1_openvpn-client-config.ovpn
#echo ""  >> openvpn-client-config.ovpn
cat certs_$1/client1.domain.tld.key >> $1_openvpn-client-config.ovpn
#echo ""  >> openvpn-client-config.ovpn
echo '</key>' >> $1_openvpn-client-config.ovpn
echo ""  >> $1_openvpn-client-config.ovpn

# Append server to DNS name
sed -i '' 's/cvpn-endpoint/server.cvpn-endpoint/g' $1_openvpn-client-config.ovpn
