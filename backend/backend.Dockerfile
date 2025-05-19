# Stage 1: install Python dependencies
FROM python:3.11-slim AS backend-build
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the whole backend tree
COPY . /app/backend

# tell Python to look for “backend” under /app
ENV PYTHONPATH=/app

# Expose port and run app
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
