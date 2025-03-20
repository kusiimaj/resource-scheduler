# official lightweight Python image
FROM python:3.9-slim

# working directory inside the container
WORKDIR /app

#  backend files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt



# Expose the application port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
