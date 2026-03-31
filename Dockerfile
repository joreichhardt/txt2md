# Use a lightweight Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set environment variables (defaults)
ENV PORT=5000
ENV FLASK_DEBUG=False
ENV GEMINI_API_KEY=""
ENV FLASK_SECRET_KEY="production-secret-key-change-me"

# Expose the application port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
