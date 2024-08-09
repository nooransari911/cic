 #Use an official base image
FROM python:3.11-alpine

# Set the working directory
WORKDIR /app

# Copy the application code to the container
COPY ./*.py /app
COPY ./requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run the application
# docker container run -p x:8000 comm-im
EXPOSE 8000
CMD ["gunicorn", "main:app"]
