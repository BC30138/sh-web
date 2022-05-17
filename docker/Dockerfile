# pull official base image
FROM python:3.9.5-slim-buster

# Install packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++

# set work directory
WORKDIR /opt/webapp
EXPOSE 5000

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn==20.1.0

# Install project
COPY docker/start.sh start.sh
COPY . .

# Add user and change user
RUN chown -R nobody:nogroup .
USER nobody

# Run app
CMD ["./start.sh"]