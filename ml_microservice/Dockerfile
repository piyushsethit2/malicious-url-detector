# Multi-stage build for maximum optimization
FROM python:3.9-alpine AS build

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    linux-headers \
    && rm -rf /var/cache/apk/*

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage - Use minimal Alpine
FROM python:3.9-alpine

# Install only runtime dependencies
RUN apk add --no-cache \
    curl \
    && rm -rf /var/cache/apk/*

# Set working directory
WORKDIR /app

# Copy Python packages from build stage
COPY --from=build /root/.local /root/.local

# Copy application code
COPY . .

# Create a non-root user for security
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup && \
    chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Add user packages to PATH
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE 5001

# Set environment variables
ENV PORT=5001
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Run the application
CMD ["python3", "app.py"] 