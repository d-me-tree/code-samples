FROM python:3.6.5-slim-jessie
MAINTAINER Dimitri Denisjonok <dimitri.781@gmail.com>

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt && pip install -e .

ENV PYTHONPATH="/app"

CMD ["bash"]
