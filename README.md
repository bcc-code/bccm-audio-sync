# Audio Sync API

A simple REST API for synchronizing two audio files using cross-correlation analysis.

## Features

- Sync two audio files by finding their time offset using file paths
- Support for multiple audio formats (WAV, MP3, MP4, FLAC, M4A, AAC)
- Modular architecture with separate processing logic
- Dockerized for easy deployment using UV package manager
- Simple REST API interface with JSON payloads
- Automatic file format handling with FFmpeg

## Architecture

- `audio_sync.py`: Core audio processing module with `AudioSyncProcessor` class
- `app.py`: Thin Flask wrapper providing REST API endpoints
- `pyproject.toml`: UV-based dependency management

## Quick Start with Docker

1. Build the Docker image:
```bash
docker build -t audio-sync-api .
```

2. Run the container:
```bash
docker run -p 5000:5000 audio-sync-api
```

3. The API will be available at `http://localhost:5000`

## API Endpoints

### `POST /sync`
Synchronize two audio files using local file paths.

**Request:** JSON payload:
```json
{
  "reference_file": "/path/to/reference.wav",
  "target_file": "/path/to/target.wav",
  "output_dir": "/path/to/output" // optional
}
```

**Response:**
```json
{
  "success": true,
  "offset_seconds": -2.345,
  "reference_file": "/path/to/reference.wav",
  "target_file": "/path/to/target.wav",
  "output_file": "/path/to/output/target_synced.wav",
  "command": "ffmpeg -i target.wav -ss 2.345 -c copy -y output.wav",
  "message": "Files synced successfully. Offset: -2.345s"
}
```

### `POST /info`
Get information about an audio file.

**Request:** JSON payload:
```json
{
  "file_path": "/path/to/audio.wav"
}
```

**Response:**
```json
{
  "file_path": "/path/to/audio.wav",
  "duration_seconds": 180.5,
  "exists": true,
  "format": ".wav"
}
```

### `GET /health`
Health check endpoint.

### `GET /`
API documentation and info.

## Usage Examples

```bash
# Sync two audio files
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"reference_file": "/data/reference.wav", "target_file": "/data/target.wav"}' \
  http://localhost:5000/sync

# Get file information
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"file_path": "/data/audio.wav"}' \
  http://localhost:5000/info
```

## Local Development

1. Install UV (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install dependencies:
```bash
uv sync
```

3. Run the Flask app:
```bash
uv run python app.py
```

## Module Usage

You can also use the audio sync functionality directly:

```python
from audio_sync import sync_audio_files, AudioSyncProcessor

# Simple function usage
result = sync_audio_files('/path/to/reference.wav', '/path/to/target.wav')

# Class-based usage
processor = AudioSyncProcessor()
result = processor.sync_files('/path/to/reference.wav', '/path/to/target.wav')
info = processor.get_file_info('/path/to/audio.wav')
```

## How It Works

1. Loads both audio files using librosa
2. Resamples to match sample rates if needed
3. Performs cross-correlation to find the optimal time offset
4. Uses FFmpeg to apply the offset:
   - If target file starts later: adds silence at the beginning
   - If target file starts earlier: cuts from the beginning
   - If files are aligned: copies the file

## Supported Formats

- WAV
- MP3
- MP4
- FLAC
- M4A
- AAC

## Requirements

- Python 3.9+
- FFmpeg (for audio processing)
- UV package manager
