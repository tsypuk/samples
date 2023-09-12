resource "aws_acm_certificate" "vpn_server" {
  private_key       = file("${var.cert_dir}_${local.region}/server.key")
  certificate_body  = file("${var.cert_dir}_${local.region}/server.crt")
  certificate_chain = file("${var.cert_dir}_${local.region}/ca.crt")

  tags = local.global_tags

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate" "vpn_client" {
  private_key       = file("${var.cert_dir}_${local.region}/client1.domain.tld.key")
  certificate_body  = file("${var.cert_dir}_${local.region}/client1.domain.tld.crt")
  certificate_chain = file("${var.cert_dir}_${local.region}/ca.crt")

  tags = local.global_tags
}

resource "aws_security_group" "vpn_access" {
  vpc_id = aws_vpc.main.id
  name   = "ovpn-sg"

  ingress {
    from_port   = 443
    protocol    = var.transport_protocol
    to_port     = 443
    cidr_blocks = [
      "0.0.0.0/0"
    ]
    description = "Incoming VPN connection"
  }

  egress {
    from_port   = 0
    protocol    = "-1"
    to_port     = 0
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  tags = local.global_tags
}

resource "aws_ec2_client_vpn_endpoint" "vpn" {
  description            = "Client VPN example"
  client_cidr_block      = var.vpn_client_CIDR
  split_tunnel           = var.split_tunnel
  server_certificate_arn = aws_acm_certificate.vpn_server.arn

  authentication_options {
    type                       = "certificate-authentication"
    root_certificate_chain_arn = aws_acm_certificate.vpn_client.arn
  }

  dns_servers = var.dns_servers

  connection_log_options {
    enabled = false
  }

  tags = local.global_tags
}

resource "aws_ec2_client_vpn_network_association" "vpn_subnets" {
  client_vpn_endpoint_id = aws_ec2_client_vpn_endpoint.vpn.id
  subnet_id              = aws_subnet.sn_az.id
  security_groups        = [aws_security_group.vpn_access.id]

  lifecycle {
    // The issue why we are ignoring changes is that on every change
    // terraform screws up most of the vpn assosciations
    // see: https://github.com/hashicorp/terraform-provider-aws/issues/14717
    ignore_changes = [subnet_id]
  }
}

resource "aws_ec2_client_vpn_authorization_rule" "vpn_auth_rule" {
  client_vpn_endpoint_id = aws_ec2_client_vpn_endpoint.vpn.id
  target_network_cidr    = "0.0.0.0/0"
  authorize_all_groups   = true
}

resource "aws_ec2_client_vpn_route" "vpn_routes" {
  client_vpn_endpoint_id = aws_ec2_client_vpn_endpoint.vpn.id
  destination_cidr_block = "0.0.0.0/0"
  target_vpc_subnet_id   = aws_subnet.sn_az.id
  depends_on             = [
    aws_ec2_client_vpn_endpoint.vpn,
    aws_ec2_client_vpn_network_association.vpn_subnets
  ]
}

#resource "null_resource" "create-client-vpn-route" {
#  provisioner "local-exec" {
#    command = "aws --region ${local.region} ec2 create-client-vpn-route --client-vpn-endpoint-id ${aws_ec2_client_vpn_endpoint.vpn.id} --destination-cidr-block 0.0.0.0/0 --target-vpc-subnet-id ${aws_subnet.sn_az.id} --description Internet-Access"
#  }
#
#  depends_on = [
#    aws_ec2_client_vpn_endpoint.vpn,
#    aws_ec2_client_vpn_network_association.vpn_subnets
#  ]
#}

resource "null_resource" "export-client-config" {
  provisioner "local-exec" {
    command = "aws --region ${local.region} ec2 export-client-vpn-client-configuration --client-vpn-endpoint-id ${aws_ec2_client_vpn_endpoint.vpn.id} --output text>${path.root}/${local.region}_openvpn-client-config.ovpn"
  }

  depends_on = [
    aws_ec2_client_vpn_endpoint.vpn,
    #    null_resource.create-client-vpn-route,
    aws_ec2_client_vpn_route.vpn_routes,
    aws_ec2_client_vpn_network_association.vpn_subnets,
  ]
}

resource "null_resource" "patch_vpn_config_locally" {
  provisioner "local-exec" {
    command = "${path.root}/patch_certs.sh ${local.region}"
  }

  depends_on = [
    aws_ec2_client_vpn_authorization_rule.vpn_auth_rule,
    null_resource.export-client-config
  ]
}
