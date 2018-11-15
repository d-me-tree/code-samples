# boto3
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/boto3.html

import boto3

########################################################################################################################
# Client or Resource
#
# Boto3 offers two distinct ways of accessing AWS APIs:#
#   - client: low-level service access
#   - resource: higher-level object-oriented service access
#
# The available resources are:
#    - cloudformation
#    - cloudwatch
#    - dynamodb
#    - ec2
#    - glacier
#    - iam
#    - opsworks
#    - s3
#    - sns
#    - sqs
#
# NOTE: you can access the client directly via the resource like so: `resource.meta.client`.
#
# Links:
#   https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html
#   https://realpython.com/python-boto3-aws-s3/
########################################################################################################################


########################################################################################################################
# How to choose an AWS profile when using boto3?
#
# First, configure awc cli: https://docs.aws.amazon.com/cli/latest/userguide/cli-multiple-profiles.html
#
# E.g. the content of ~/.aws/config
# [default]
# region = eu-west-1
# output = json
#
# [profile boto3user]
# region = eu-west-2
# output = json
#
# Links:
#   https://stackoverflow.com/a/33395432
########################################################################################################################

session = boto3.Session(profile_name='boto3user')
ecs_client = session.client('ecs')
