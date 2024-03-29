# Samples for posts and articles:

## x86-64 vs arm-64 benchmark results

- [arm](perftest-instance/results/arm)
- [x86](perftest-instance/results/x86)
- 
## EC2 VoIP Asterisk & FreePBX

- [ec2_asterisk.sh](asterisk/ec2_asterisk.sh)
- [ec2_freepbx.sh](asterisk/ec2_freepbx.sh)

## S3 pre-signed URLs with reverse engineering

[reverse-engineer.py](s3-signed/reverse-engineer.py)

## AWS MachineLearning Comprehend & Rekongnition

![augmented-200_70.png](aws_hlml/rekognition/augmented-200_70.png)

- Jypyter Notebooks:[sa.ipynb](aws_hlml/rekognition/sa.ipynb)
- Jypyter Notebooks:[aws_comprehend.ipynb](aws_hlml/comprehend/aws_comprehend.ipynb)
- Date: 16.11.2023

## Terraform IaC (AWS API gateway with AWS_IAM auth type for HTTP endpoint)

![api-gw-iam.png](https://blog.tsypuk.com/images/posts/aws-apigw-iam/api-gw-iam.png)

- Files: [main.tf](apigw/main.tf) [output.tf](apigw/output.tf)
- Post in Blog: [https://tsypuk.github.io/posts/2023/06/24/api-gw-iam.html](https://tsypuk.github.io/posts/2023/06/24/api-gw-iam.html)
- Date: 25.06.2023

## Terraform IaC (Client VPN)

![clien_vpn.png](https://blog.tsypuk.com/images/posts/vpn/infra.png)

- Generate Client&Server certificates for VPN connection: [gen_certs.sh](client-vpn/gen_certs.sh)
- Patch AWS OpenVPN configuration: [patch_certs.sh](client-vpn/patch_certs.sh)
- Terraform: [vpc.tf](client-vpn/vpc.tf) [vpn.tf](client-vpn/vpn.tf) [output.tf](client-vpn/output.tf)
- Post in Blog: [https://blog.tsypuk.com/posts/2023/09/11/aws-clientnpv-automated.html)
- Date: 11.09.2023

## CloudFormation IaC (DynamoDB)

![dynamodb.png](https://blog.tsypuk.com/images/posts/dynamo/diagram.png)

- NoSQL Workbench Export for Movies Table [nosql_workbench_export.json](dynamodb/Movies.json)
- CloudFormation Template: [dynamodb_cf_template.json](dynamodb/movies_cf_template.json)
- Post in Blog: [https://blog.tsypuk.com/posts/2023/10/01/dynamo-design.html)
- Date: 03.10.2023

## CloudFormation IaC (DynamoDB One-To-Many)

![dynamodb.png](https://blog.tsypuk.com/images/posts/dynamo/diagram2.png)

- NoSQL Workbench Export for Movies Table [nosql_workbench_export.json](dynamodb/Users.json)
- CloudFormation Template: [dynamodb_cf_template.json](dynamodb/Users_cf_template.json)
- Post in Blog: [https://blog.tsypuk.com/posts/2023/10/04/dynamo-one-to-many.html](https://blog.tsypuk.com/posts/2023/10/04/dynamo-one-to-many.html)
- Date: 04.10.2023

## CloudFormation IaC (DynamoDB Filtering)

![dynamodb.png](https://blog.tsypuk.com/images/posts/dynamo/diagram3.png)

- NoSQL Workbench Export for Movies Table [nosql_workbench_export.json](dynamodb-filter/Users.json)
- CloudFormation Template: [dynamodb_cf_template.json](dynamodb-filter/Users_cf_template.json)
- Post in Blog: [https://blog.tsypuk.com/posts/2023/10/06/dynamo-filters.html](https://blog.tsypuk.com/posts/2023/10/06/dynamo-filters.html)
- Date: 07.10.2023

## Terraform IaC (Kinesis Firehose with S3)

![kinesis.png](https://blog.tsypuk.com/images/posts/kinesis/infra.png)

- Terraform Template: [firehose.tf](kinesis-agent/firehose.tf)
- Post in Blog: [https://blog.tsypuk.com/posts/2023/10/17/kineses-agent.html)
- Date: 05.10.2023