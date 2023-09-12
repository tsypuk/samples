# Samples for posts and articles:

## Terraform IaC (AWS API gateway with AWS_IAM auth type for HTTP endpoint)

![infra.png](apigw/infra.png)

- Files: [main.tf](apigw/main.tf) [output.tf](apigw/output.tf)
- Post in Blog: [https://tsypuk.github.io/posts/2023/06/24/api-gw-iam.html](https://tsypuk.github.io/posts/2023/06/24/api-gw-iam.html)
- Date: 25.06.2023

## Terraform IaC (Client VPN)

![infra.png](client-vpn/infra.png)

- Generate Client&Server certificates for VPN connection: [gen_certs.sh](client-vpn/gen_certs.sh)
- Patch AWS OpenVPN configuration: [patch_certs.sh](client-vpn/patch_certs.sh)
- Terraform: [vpc.tf](client-vpn/vpc.tf) [vpn.tf](client-vpn/vpn.sh) [output.tf](client-vpn/output.tf)
- Date: 11.09.2023
