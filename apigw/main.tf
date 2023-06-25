data "aws_caller_identity" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
}

provider "aws" {
  alias = "region"
}

data "aws_region" "current" {
  provider = "aws.region"
}

resource "aws_api_gateway_rest_api" "sigv4_rest_api" {
  body = jsonencode({
    openapi = "3.0.1"
    info    = {
      title   = "SigV4 verification"
      version = "1.0"
    }
    paths = {
      "/path1" = {
        get = {
          security : [
            {
              sigv4 : []
            }
          ]
          x-amazon-apigateway-integration = {
            httpMethod           = "GET"
            payloadFormatVersion = "1.0"
            type                 = "HTTP_PROXY"
            uri                  = "https://ip-ranges.amazonaws.com/ip-ranges.json"
          }
        }
      }
    }
    components = {
      securitySchemes = {
        sigv4 = {
          type                         = "apiKey"
          name                         = "Authorization"
          in : "header"
          x-amazon-apigateway-authtype = "awsSigv4"
        }
      }
    }
  }
  )


  description = "API Gateway"
  name        = "Regional API GW with 'AWS IAM' auth type"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

# Deployment
resource "aws_api_gateway_deployment" "prod-deployment" {
  rest_api_id = aws_api_gateway_rest_api.sigv4_rest_api.id

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.sigv4_rest_api.body))
  }

  lifecycle {
    create_before_destroy = true
  }

}

resource "aws_api_gateway_stage" "PROD" {
  deployment_id        = aws_api_gateway_deployment.prod-deployment.id
  rest_api_id          = aws_api_gateway_rest_api.sigv4_rest_api.id
  stage_name           = "PROD"
  xray_tracing_enabled = true
}

# Programmatic IAM user
resource "aws_iam_user" "user" {
  name = "api-caller"
  path = "/"
}

resource "aws_iam_user_policy" "apigw_invoke_policy_inline" {
  name = "allow-invoke-get-method-policy"
  user = aws_iam_user.user.name

  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Action = [
          "execute-api:Invoke",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:execute-api:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.sigv4_rest_api.id}/${aws_api_gateway_stage.PROD.stage_name}/GET/path1"
      },
    ]
  })
}
