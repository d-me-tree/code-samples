#!/usr/bin/env bash

# https://github.com/nicor88/insert-to-db.python.lambda/blob/master/Makefile

# Clean
rm -rf build
rm -rf dist

# Install
mkdir build

# https://hub.docker.com/r/lambci/lambda/
docker run --rm \
--entrypoint pip \
-v "$PWD":/var/task \
-it \
lambci/lambda:python3.6 \
install -r requirements.txt -t build

# Copy
cp -R src/lambda_function.py build/

# Zip
mkdir dist
cd build && zip -rq ../dist/lambda.zip .

# Upload
# cd .. && aws s3 cp dist/lambda.zip s3://lmbda-src/181115-lambda.zip

# Clean
rm -rf build
