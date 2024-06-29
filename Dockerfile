# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file from the rangam_ai folder into the container
COPY rangam_ai/requirements.txt /app/rangam_ai/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r /app/rangam_ai/requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port (if your application uses a specific port)
EXPOSE 8000

# Set environment variables
ENV OPENAI_APIKEY=${OPENAI_APIKEY}

# Run the command to start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
