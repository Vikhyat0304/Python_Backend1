# Base image
FROM python:3.11-slim

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /code/

# Run FastAPI by default
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
