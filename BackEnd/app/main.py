from fastapi import FastAPI
from app.api.v1 import routes_auth, routes_events, routes_facilities, routes_users, routes_animals

app = FastAPI(
    title="Farm Traceability System",
    description="Trace animal and product lifecycle events with plausibility validation.",
    version="1.0.0",
)

# Routers
app.include_router(routes_auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(routes_facilities.router, prefix="/api/v1/facilities", tags=["Facilities"])
app.include_router(routes_events.router, prefix="/api/v1/events", tags=["Events"])
app.include_router(routes_users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(routes_animals.router, prefix="/api/v1/animals", tags=["Animals"])

@app.get("/")
def root():
    return {"message": "Welcome to the Farm Traceability API"}
