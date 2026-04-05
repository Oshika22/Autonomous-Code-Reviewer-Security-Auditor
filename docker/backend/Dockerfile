# Base image: lightweight, fixed Python version for reproducibility 
FROM python:3.11-slim

# Security: create a non-root user
# Containers run as root by default; a non-root user limits damage
# if any vulnerability is exploited inside the container.
RUN useradd -m appuser

# Set working directory
WORKDIR /app



# System dependencies
# gcc is required by some Python packages that compile C extensions
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# ── Install Python dependencies (layer-cached separately)
# Copying requirements.txt first means Docker reuses this layer
# on rebuilds if only source code changed — significantly faster.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container 
COPY . .

# Fix file ownership for the non-root user 
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port for future API/frontend integration
EXPOSE 8000

# Entrypoint: run the security auditor 
# rag/main.py is the correct path relative to WORKDIR /app
CMD ["python", "rag/main.py"]
