# FarmTrack Backend

FastAPI-based backend for the FarmTrack livestock traceability system.

## Database Seeding

The database is automatically seeded with sample data when the containers are built. The seeder includes:

- **Users**: 7 sample users (farmers, processors, regulators)
- **Facilities**: 10 sample facilities (farms, processors, retailers)
- **Animal Breeds**: 15,705+ breeds loaded from CSV (includes global livestock breeds)
- **Animals**: 50 sample animals
- **Events**: 200 sample traceability events

### Breed Data

Animal breed data is loaded from `app/data/animal_breeds.csv`, which contains comprehensive livestock breed information from around the world, including:
- Country of origin
- ISO3 country code
- Species (Cattle, Sheep, Goat, Pig, Chicken, Horse, etc.)
- Breed name and alternative names
- Language and descriptions
- Transboundary breed names

### Running the Seeder

The database is seeded automatically when you rebuild the containers:

```bash
docker-compose down -v  # Remove existing database
docker-compose up --build -d  # Rebuild and start
```

Or manually run the seeder:

```bash
docker exec traceability_api python -m app.db.seed_data
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login

### Dashboard
- `GET /api/v1/dashboard/overview` - Dashboard statistics
- `GET /api/v1/dashboard/recent-events` - Recent traceability events
- `GET /api/v1/dashboard/timeline` - Event timeline data
- `GET /api/v1/dashboard/top-facilities` - Top facilities by animal count
- `GET /api/v1/dashboard/species-distribution` - Animal species breakdown

### Animals
- `GET /api/v1/animals/` - List all animals
- `POST /api/v1/animals/` - Create new animal
- `GET /api/v1/animals/{id}` - Get animal details
- `PUT /api/v1/animals/{id}` - Update animal
- `DELETE /api/v1/animals/{id}` - Delete animal
- `GET /api/v1/animals/{id}/events` - Get animal's events
- `GET /api/v1/animals/species` - List all species
- `GET /api/v1/animals/stats` - Animal statistics

### Facilities
- `GET /api/v1/facilities/` - List all facilities
- `POST /api/v1/facilities/` - Create new facility
- `GET /api/v1/facilities/{id}` - Get facility details
- `PUT /api/v1/facilities/{id}` - Update facility
- `DELETE /api/v1/facilities/{id}` - Delete facility
- `GET /api/v1/facilities/types` - List facility types
- `GET /api/v1/facilities/{id}/animals` - Get facility's animals
- `GET /api/v1/facilities/stats` - Facility statistics

### Events
- `GET /api/v1/events/` - List events (supports filtering)
- `POST /api/v1/events/` - Create new event
- `GET /api/v1/events/types` - List event types
- `GET /api/v1/events/anomalies` - List anomalies (invalid events)
- `GET /api/v1/events/stats` - Event statistics

### Users
- `GET /api/v1/users/` - List all users
- `POST /api/v1/users/` - Create new user
- `GET /api/v1/users/{id}` - Get user details
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

## Database Models

### User
- username
- password_hash
- role (farmer, processor, regulator)

### Facility
- name
- location
- facility_type (farm, processor, retailer)

### Animal
- name
- species
- tag_id (unique)
- date_added
- facility_id
- owner_id

### AnimalBreed
- country
- iso3
- specie
- breed_name
- language
- description
- transboundary_name
- other_name

### Event
- event_type
- animal_id
- actor_id
- facility_id
- timestamp
- event_metadata
- is_valid
- anomaly_reason

## Configuration

Environment variables are configured in `docker-compose.yml`:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT token signing key
