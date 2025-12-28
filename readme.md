# 4chan-Post-Generator

Forked from LeoViguier/greentext-maker.

A web app that creates fake 4chan posts from text, and then gives you a series of mobile-friendly screenshots for uploading to other social media sites.

# Installing

## Docker Run:

```bash
docker run -p 8501:8501 ghcr.io/lankyfemme/4chan-post-generator
```

## Docker Compose (recommended):

```yaml
services:
    4chan-post-generator:
        image: ghcr.io/lankyfemme/4chan-post-generator
        container_name: 4chan-post-generator
        restart: unless-stopped
        posts:
            - 8501:8501
```

# Usage:

Go to the device's IP (if you're running the container on your own machine, `localhost`), port 8501.

**For example**: `127.0.0.1:8501`

