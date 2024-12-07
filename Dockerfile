# Use an official Python image as the base
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install system dependencies (if necessary)
RUN apt-get update && apt-get install -y netcat-openbsd

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the wait-for-it.sh script to the container
COPY wait-for-it.sh /usr/src/app/wait-for-it.sh

RUN chmod +x /usr/src/app/wait-for-it.sh

# Expose port 8000 for the Django development server
EXPOSE 8000

# Define the command to run the app with wait-for-it to wait for PostgreSQL
CMD ["sh", "-c", "/usr/src/app/wait-for-it.sh postgres:5432 -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
