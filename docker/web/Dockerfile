# pull official base image
FROM python:3.9.5-slim-buster

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /opt/webapp

# copy project
COPY . .

# Install packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn==20.1.0

# Install project
COPY docker/web/artifacts.sh artifacts.sh
COPY docker/web/start.sh start.sh

# Add user and change user
RUN chown -R nobody:nogroup .
USER nobody

# Compile artifacts
RUN ./artifacts.sh

# Run app
CMD ["./start.sh"]
