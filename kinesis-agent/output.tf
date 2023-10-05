output "kinesis_firehose" {
  value = aws_kinesis_firehose_delivery_stream.extended_s3_stream.id
}