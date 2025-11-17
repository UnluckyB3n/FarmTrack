from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import routes_auth, routes_events, routes_facilities, routes_users, routes_animals, routes_dashboard, routes_settings, routes_breeds, routes_documents, routes_reports
from app.db.init_db import init_db

app = FastAPI(
    title="FarmTrack API",
    description="""
    ## Farm Traceability System API
    
    A comprehensive livestock traceability system for tracking animals, events, and supply chain movements.
    
    ### Features
    
    * **Authentication**: JWT-based authentication with role-based access control
    * **Animal Management**: Track animals with breeds, facilities, and ownership
    * **Event Tracking**: Record lifecycle events (birth, vaccination, movement, etc.)
    * **Facility Management**: Manage farms, processors, and retailers
    * **Document Management**: Upload and store vaccination records, certificates, and test results
    * **QR Code Generation**: Generate QR codes for public animal traceability
    * **Movement Tracking**: Track animal transfers between facilities
    * **Anomaly Detection**: Automatic plausibility validation for events
    * **Dashboard Analytics**: Overview statistics and recent activity
    
    ### Authentication
    
    Most endpoints require JWT authentication. Use the `/api/v1/auth/login` endpoint to obtain a token.
    
    Include the token in requests using the `Authorization` header:
    ```
    Authorization: Bearer <your_token>
    ```
    
    ### User Roles
    
    - **farmer**: Can manage their own animals and facilities
    - **processor**: Can process animals and manage processing facilities
    - **regulator**: Can view all data for compliance and auditing
    """,
    version="1.0.0",
    contact={
        "name": "FarmTrack Support",
        "email": "support@farmtrack.example.com",
    },
    license_info={
        "name": "MIT License",
    },
    openapi_tags=[
        {
            "name": "Auth",
            "description": "Authentication and user registration endpoints"
        },
        {
            "name": "Animals",
            "description": "Manage animals, track movements, and generate QR codes"
        },
        {
            "name": "Events",
            "description": "Record and query lifecycle events for animals"
        },
        {
            "name": "Facilities",
            "description": "Manage farms, processors, and retail facilities"
        },
        {
            "name": "Documents",
            "description": "Upload and manage documents (vaccination records, certificates)"
        },
        {
            "name": "Breeds",
            "description": "Browse animal breed database with 15,000+ breeds"
        },
        {
            "name": "Users",
            "description": "User management endpoints"
        },
        {
            "name": "Dashboard",
            "description": "Analytics and overview statistics"
        },
        {
            "name": "Settings",
            "description": "User profile and account settings"
        },
        {
            "name": "Reports",
            "description": "PDF export for traceability reports and audit logs"
        }
    ]
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
app.include_router(routes_documents.router, prefix="/api/v1", tags=["Documents"])
app.include_router(routes_reports.router, prefix="/api/v1/reports", tags=["Reports"])

@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint - API information.
    
    Returns welcome message and links to documentation.
    """
    return {
        "message": "Welcome to the FarmTrack API",
        "version": "1.0.0",
        "documentation": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json"
    }


@app.get("/health", tags=["Root"])
def health_check():
    """
    Health check endpoint.
    
    Returns API status and version information.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "FarmTrack API"
    }
