# Use an official Python runtime as a parent image
FROM python:3.10-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Run your application
CMD ["python", "__main__.py"]
