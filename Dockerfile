# Dockerfile

FROM python:3.10-slim

# Set the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the entrypoint script into the image
COPY entrypoint.sh /code/

# Copy the Django project
COPY . /code/

# Make entrypoint.sh executable
RUN chmod +x /code/entrypoint.sh


