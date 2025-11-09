# Stop and remove existing containers and volumes
docker-compose down -v
# Build and start the containers
docker-compose up --build
# Start containers
docker-compose up -d
# Setup database and seed data
Start-Sleep -Seconds 10; docker exec traceability_api python -m app.db.seed_data
# Run unit tests
docker-compose exec backend python -m pytest tests/ -v