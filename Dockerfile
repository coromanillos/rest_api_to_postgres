# Official Python image as base
FROM python:3.10-slim

# Set working directory as container
WORKDIR /app

# Copy requirements.txt to container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Define the comand to run the application
CMD ["python", "app.py"]
