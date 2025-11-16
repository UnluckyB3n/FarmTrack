from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import routes_auth, routes_events, routes_facilities, routes_users, routes_animals, routes_dashboard, routes_settings, routes_breeds
from app.db.init_db import init_db

app = FastAPI(
    title="Farm Traceability System",
    description="Trace animal and product lifecycle events with plausibility validation.",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost",
        "http://127.0.0.1"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Routers
app.include_router(routes_auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(routes_facilities.router, prefix="/api/v1/facilities", tags=["Facilities"])
app.include_router(routes_events.router, prefix="/api/v1/events", tags=["Events"])
app.include_router(routes_users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(routes_animals.router, prefix="/api/v1/animals", tags=["Animals"])
app.include_router(routes_dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(routes_settings.router, prefix="/api/v1/settings", tags=["Settings"])
app.include_router(routes_breeds.router, prefix="/api/v1/breeds", tags=["Breeds"])

@app.get("/")
def root():
    return {"message": "Welcome to the Farm Traceability API"}
