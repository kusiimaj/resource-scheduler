# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all backend files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run tests inside the container
RUN pytest tests/ || exit 1

# Expose the application port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
