# A sandboxed local environment that replicates the live AWS Lambda environment
# https://hub.docker.com/r/lambci/lambda/
FROM lambci/lambda:build-python3.6
MAINTAINER Dimitri Denisjonok <dimitri.781@gmail.com>

# WORKDIR /var/task

WORKDIR /app

COPY requirements.txt /app/
COPY src/lambda_function.py /app/build/

RUN pip install -r requirements.txt -t build && \
    cd build && zip -r ../lambda.zip .

CMD ["bash"]
