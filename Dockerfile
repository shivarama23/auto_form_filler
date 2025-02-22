# Stage 1: Backend setup
FROM python:3.10-slim as backend

# Set the working directory
WORKDIR /app

# Copy backend code
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend /app

# Copy the frontend code
COPY frontend /frontend  
# Add this line to copy the frontend directory

# Expose the application port
EXPOSE 8000

# Command to run FastAPI
CMD ["/app/start.sh"]
