output "invoke_url" {
  value = aws_api_gateway_stage.PROD.invoke_url
}

output "endpoint_configuration" {
  value = aws_api_gateway_rest_api.sigv4_rest_api.endpoint_configuration
}

output "api_gw_arn" {
  value = aws_api_gateway_rest_api.sigv4_rest_api.arn
}

output "user_arn" {
  value = aws_iam_user.user.*.arn
}
