# Stage 1
FROM python:3.11-slim AS base
FROM base AS builder

WORKDIR /app

#Copying only requirements - the layer will be cached till the file changes
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --default-timeout=1000 \
    --prefix=/install \
    -r requirements.txt

FROM base

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=builder /install /usr/local

COPY src/ ./src/

RUN useradd -m voiduser && \
    chown -R voiduser:voiduser /app

USER voiduser

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
