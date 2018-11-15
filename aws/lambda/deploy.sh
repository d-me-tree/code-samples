#!/usr/bin/env bash

# aws lambda create-function \
# --region eu-west-1 \
# --function-name PandasVersion  \
# --code S3Bucket=lmbda-src,S3Key=181115-lambda.zip \
# --role arn:aws:iam::149681194111:role/lambdaVPCExecutionRole \
# --handler lambda_function.lambda_handler \
# --runtime python3.6 \
# --vpc-config SubnetIds=subnet-48ca111c,SecurityGroupIds=sg-8b48a1d1

# Test: invoke manually
aws lambda invoke \
--function-name PandasVersion  \
--region eu-west-1 \
output.txt
