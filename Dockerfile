# Stage 1: Build stage
FROM python:3.9-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.9-slim

# Install curl for health check and create non-root user
RUN apt-get update && apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m -u 1000 pythonuser

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder --chown=pythonuser:pythonuser /root/.local /home/pythonuser/.local
COPY --chown=pythonuser:pythonuser src/ ./src/

# Switch to non-root user
USER pythonuser

# Make sure scripts in .local are usable
ENV PATH=/home/pythonuser/.local/bin:$PATH

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]
