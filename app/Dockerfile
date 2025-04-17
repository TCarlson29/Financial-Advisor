FROM python:3.9-alpine

WORKDIR /app

# Copy only what we need for a clean build
COPY requirements.txt .

# Install everything, including uvicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY main.py .

# Expose the port your app listens on
EXPOSE 8000

# Run with the exec form so signals are handled properly
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
