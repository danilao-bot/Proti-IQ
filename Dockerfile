# Multi-stage secure Dockerfile for Proti IQ
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime image
FROM python:3.11-slim AS runner

WORKDIR /app

# Create non-root system user
RUN useradd -m -u 1001 proti_user

COPY --from=builder /root/.local /home/proti_user/.local
ENV PATH=/home/proti_user/.local/bin:$PATH

COPY . .
RUN chown -R proti_user:proti_user /app

USER proti_user

EXPOSE 8000 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
