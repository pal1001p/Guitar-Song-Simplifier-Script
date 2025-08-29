# Guitar Song Simplifier - Docker 

This Docker setup transforms audio processing scripts into a FastAPI backend server.

## Quick Start

### 1. Build and Run with Docker Compose (Recommended)

```bash
# Build and start the service
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop the service
docker-compose down
```

### 2. Build and Run with Docker

```bash
# Build the image
docker build -t guitar-song-simplifier .

# Run the container
docker run -p 8000:8000 guitar-song-simplifier
```

## API Endpoints

Once running, the API will be available at `http://localhost:8000`

### Endpoints:

- `GET /` - Root endpoint with API info
- `GET /health` - Health check
- `POST /analyze-audio/` - Upload and analyze audio file

### Example Usage:

```bash
# Test the API
curl http://localhost:8000/health

# Upload and analyze an audio file
curl -X POST "http://localhost:8000/analyze-audio/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_audio_file.wav"
```

## Testing

Use the provided test script:

```bash
# Test basic endpoints
python test_api.py

# Test with an audio file
python test_api.py /path/to/your/audio.wav
```

## API Response Format

The `/analyze-audio/` endpoint returns:

```json
{
  "beats": [0.5, 1.0, 1.5, 2.0, ...],
  "beat_count": 200,
  "file_info": {
    "filename": "song.wav",
    "content_type": "audio/wav",
    "size_bytes": 1234567
  }
}
```

## Development

### Local Development with Docker

```bash
# Start with volume mounting for live code changes
docker-compose up --build

# The src/ directory is mounted as read-only for development
```

### Adding New Features

1. Modify the code in `src/`
2. Update `main.py` in the Dockerfile to import your new functions
3. Rebuild: `docker-compose up --build`

## Production Deployment

### Environment Variables

Set these for production:

```bash
# In docker-compose.yml or docker run command
environment:
  - CORS_ORIGINS=https://yourdomain.com
  - LOG_LEVEL=info
```

### Security Considerations

1. Update CORS settings in `main.py` for production
2. Add authentication if needed
3. Use HTTPS in production
4. Set proper file upload limits

### Scaling

For high traffic, consider:
- Using a reverse proxy (nginx)
- Load balancing multiple containers
- Using a CDN for static files
- Implementing caching for processed results

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in docker-compose.yml
2. **Memory issues**: Increase Docker memory limits for large audio files
3. **Build failures**: Check that all dependencies are in requirements.txt

### Logs

```bash
# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs guitar-song-simplifier
```
