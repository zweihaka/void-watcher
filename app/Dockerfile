#We're using slim version for the best performance and light weight
FROM python:3.11-slim

#Setting our working directory
WORKDIR /app

#Setiing essential python environment variables for container
ENV PYTHONUNBUFFERED=1 \
    PYTHONDOWNWRITEBYTECODE=1

#Copying the list of dependencies for pip
COPY requirements.txt .

#Updating pip and installing all dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

#Copying app source code
COPY src/ ./src/

#Adding and going under different user for security
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

USER appuser

#Executing our main command for setting our backend
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
