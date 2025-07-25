# Use Python 3.11 slim image for better compatibility with scientific packages
FROM python:3.11-slim

# Install system dependencies for audio processing and UV
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install UV and verify installation in one step
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    /root/.local/bin/uv --version
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY audio_sync.py .
COPY app.py .

# Install Python dependencies using UV pip
RUN uv pip install --system flask librosa numpy scipy

# Create temp directory for file processing
RUN mkdir -p /tmp/audio_sync

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application directly with Python
CMD ["python", "app.py"]
