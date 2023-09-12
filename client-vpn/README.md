## Infra

![clien_vpn.png](https://blog.tsypuk.com/images/posts/vpn/infra.png)

## Generate Certificate 

```shell
 ./gen_certs.sh us-west-1
```

## Provision Infra

OVPN configuration download and patch is implemented in Terraform

```shell
terraform init
terraform apply
```
