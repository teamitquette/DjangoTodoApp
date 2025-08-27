# Simple Docker Setup for Django Todo App

This guide will help you build and run the Django Todo application using Docker.

## Prerequisites

- Docker installed and running on your system
- Docker Compose (usually comes with Docker Desktop)

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Start the application
docker-compose up

# Or run in background
docker-compose up -d

# Stop the application
docker-compose down

# View logs
docker-compose logs -f
```

### Option 2: Manual Docker Commands

```bash
# Build the Docker image
docker build -t todo-app .

# Run the container
docker run -p 8000:8000 todo-app

# Or run in background
docker run -d --name todo-container -p 8000:8000 todo-app
```

## Docker Compose Benefits

Using docker-compose gives you:
- **Easy management** - One command to start/stop everything
- **Development mode** - Live code reloading with volume mounting
- **Environment variables** - Easy configuration management
- **Service orchestration** - Easy to add databases, caches, etc.

## Docker Compose Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View running services
docker-compose ps

# View logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Rebuild and start
docker-compose up --build

# Stop and remove everything
docker-compose down -v
```

## Access the Application

Once running, open your browser and go to:
- **Main App**: http://localhost:8000
- **Admin**: http://localhost:8000/admin

## Container Management

### View running containers
```bash
docker-compose ps
# or
docker ps
```

### Stop container
```bash
docker-compose down
# or
docker stop todo-app
```

### Remove container
```bash
docker-compose down
# or
docker rm todo-app
```

### View container logs
```bash
docker-compose logs -f
# or
docker logs todo-app
```

### Access container shell
```bash
docker-compose exec web bash
# or
docker exec -it todo-app bash
```

## Database Setup

The first time you run the container, you'll need to set up the database:

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create admin user
docker-compose exec web python manage.py createsuperuser
```

## Development Mode

The docker-compose setup includes:
- **Volume mounting** - Your code changes are reflected immediately
- **Auto-reload** - Django development server restarts on file changes
- **Debug mode** - Full Django debug information

## Adding More Services

To add a database or other services, uncomment the relevant sections in `docker-compose.yml`:

```yaml
# Example: Add PostgreSQL
db:
  image: postgres:15-alpine
  environment:
    - POSTGRES_DB=tododb
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=postgres
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using port 8000
   netstat -ano | findstr :8000
   
   # Or use a different port in docker-compose.yml
   ports:
     - "8001:8000"
   ```

2. **Container starts but app doesn't work**
   ```bash
   # Check container logs
   docker-compose logs
   ```

3. **Database issues**
   ```bash
   # Run migrations
   docker-compose exec web python manage.py migrate
   ```

4. **Permission issues**
   ```bash
   # Rebuild the image
   docker-compose up --build
   ```

## What's Inside

This simple setup:
- Uses Python 3.11 slim image
- Installs only necessary dependencies
- Uses Django's built-in development server
- Includes health checks
- Works for both development and testing
- **Fully compatible with docker-compose**

## Next Steps

Once your container is running:
1. Open http://localhost:8000 in your browser
2. Create some todo items to test the application
3. Check the admin interface at http://localhost:8000/admin

## Support

If you encounter issues:
1. Check the container logs: `docker-compose logs`
2. Ensure Docker Desktop is running
3. Try rebuilding: `docker-compose up --build`
4. Check if the port 8000 is available on your system
