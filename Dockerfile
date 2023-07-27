# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Copy all the application files to the container
COPY main.py app.py /app/
COPY templates/ /app/templates/

# Set the entry point to run the main.py script to generate images
CMD ["python", "main.py"]

# Expose port 5000 for Flask app
EXPOSE 5000
