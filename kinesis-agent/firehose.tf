resource "aws_s3_bucket" "bucket" {
  bucket = "kinesis-logs-bucket-2023"
}

data "aws_iam_policy_document" "firehose_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["firehose.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "firehose-s3" {
  statement {
    effect  = "Allow"
    actions = ["s3:*"]

    resources = [
      aws_s3_bucket.bucket.arn,
      "${aws_s3_bucket.bucket.arn}/*",
    ]
  }
}

resource "aws_iam_role_policy" "firehose-s3" {
  name   = "s3-access"
  role   = aws_iam_role.firehose_role.id
  policy = data.aws_iam_policy_document.firehose-s3.json
}

resource "aws_iam_role" "firehose_role" {
  name               = "firehose_test_role"
  assume_role_policy = data.aws_iam_policy_document.firehose_assume_role.json
}

resource "aws_kinesis_firehose_delivery_stream" "extended_s3_stream" {
  name        = "terraform-kinesis-firehose-logs-s3-stream"
  destination = "extended_s3"

  extended_s3_configuration {
    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.bucket.arn
    buffering_size = 64
    buffering_interval = 60


    # https://docs.aws.amazon.com/firehose/latest/dev/dynamic-partitioning.html
    dynamic_partitioning_configuration {
      enabled = "false"
    }

    # Example prefix using partitionKeyFromQuery, applicable to JQ processor
    prefix              = "year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/"
    error_output_prefix = "errors/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/!{firehose:error-output-type}/"

#    processing_configuration {
#      enabled = "true"
#
#      # Multi-record deaggregation processor example
#      processors {
#        type = "RecordDeAggregation"
#        parameters {
#          parameter_name  = "SubRecordType"
#          parameter_value = "JSON"
#        }
#      }
#
#      # New line delimiter processor example
#      processors {
#        type = "AppendDelimiterToRecord"
#      }
#
      # JQ processor example
#      processors {
#        type = "MetadataExtraction"
#        parameters {
#          parameter_name  = "JsonParsingEngine"
#          parameter_value = "JQ-1.6"
#        }
#        parameters {
#          parameter_name  = "MetadataExtractionQuery"
#          parameter_value = "{customer_id:.customer_id}"
#        }
#      }
#    }
  }
}