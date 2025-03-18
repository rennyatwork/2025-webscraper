# Use official Python image from Docker Hub
FROM python:3.12-slim


# Install curl (and any other system utilities or libraries) globally
RUN apt-get update && apt-get install -y curl

# Set working directory in the container
WORKDIR /app

# Install system dependencies (if needed for scraping or other functionality)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . /app/

# Expose the ports
EXPOSE 8501
EXPOSE 8000

# Run both services in the background
CMD ["sh", "-c", "uvicorn scraper.app:app --host 0.0.0.0 --port 8000 & streamlit run app.py"]

