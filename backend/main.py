"""HRA (Hiring Resource Assistant) API.

Main FastAPI application entry point with middleware configuration
and route registration.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers.rec_routes import router as rec_router

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="HRA API",
    description="AI-powered interview recommendation engine",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rec_router, prefix="/api", tags=["recommendations"])


@app.get("/", tags=["health"])
async def root():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {"status": "ok", "service": "HRA API"}


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("HRA API starting up")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("HRA API shutting down")

