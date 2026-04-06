"""
FastAPI Finance System Backend
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes import transactions, users, analytics
import models

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="Finance System Backend",
    description="A Python-based finance tracking system with user roles and analytics",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transactions.router)
app.include_router(users.router)
app.include_router(analytics.router)


@app.get("/", tags=["root"])
def read_root():
    """
    Root endpoint for API documentation
    """
    return {
        "message": "Finance System Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "alternative_docs": "/redoc"
    }


@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Finance System Backend"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
