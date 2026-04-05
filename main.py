from fastapi import FastAPI
from database import engine, Base
import models
from routers import auth, users, admin, records, dashboard
from middleware.error_handler import add_error_handlers


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance Dashboard API",
    description="A backend system for managing financial records with role based access control",
    version="1.0.0"
)

# Add error handlers
add_error_handlers(app)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(records.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "Finance Dashboard API is running!"}

