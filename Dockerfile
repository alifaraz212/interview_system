# Image creation
FROM python:3.11-slim

# Set working directory (enter terminal of docker container)
WORKDIR /app

# Copy requirements.txt from local machine to docker container
COPY requirements.txt .

# Install packages from requirements.txt
RUN pip install -r requirements.txt

# Copy entire application code from local machine to docker container
COPY . .

# Run the application when container starts
CMD ["python", "main.py"]
