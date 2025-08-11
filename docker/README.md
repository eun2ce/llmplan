# Docker Deployment

This directory contains Docker-related files for containerizing and running the llmplan service.

## Files

- `docker-compose.yml` - Docker Compose configuration
- `nginx.conf` - Nginx reverse proxy configuration
- `README.md` - This file

## Quick Start

### Using Docker Hub Image

```bash
docker run -d \
  --name llmplan \
  -p 8000:8000 \
  -e LMSTUDIO_BASE_URL=http://host.docker.internal:1234/v1 \
  --add-host host.docker.internal:host-gateway \
  eunheejo/llmplan:latest
```

### Using Docker Compose

```bash
# From the docker/ directory
cd docker/
docker-compose up -d

# With Nginx reverse proxy
docker-compose --profile with-nginx up -d
```

## Environment Variables

| Variable            | Default                    | Description          |
| ------------------- | -------------------------- | -------------------- |
| `LMSTUDIO_BASE_URL` | `http://localhost:1234/v1` | LMStudio server URL  |
| `LMSTUDIO_API_KEY`  | `lm-studio`                | API key for LMStudio |
| `DEBUG`             | `false`                    | Enable debug mode    |

## Prerequisites

- LMStudio running on the host machine (port 1234)
- Qwen/Qwen3-4B model loaded in LMStudio
