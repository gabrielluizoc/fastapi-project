"""
Main application entry point for the Insurance API.
Configures and runs the FastAPI application with all endpoints.
"""

from fastapi import FastAPI
from src.interfaces.api.endpoints import insurance

app = FastAPI(
    title="Insurance API",
    description="""
    ## Insurance Premium Calculation Service
    
    Provides REST endpoints for calculating car insurance premiums based on:
    - Vehicle details (make, model, year, value)
    - Coverage parameters
    - Geographic risk factors (optional)
    
    ### Key Features:
    - Dynamic rate calculation
    - Broker fee integration
    - Policy limit determination
    """,
    version="1.0.0",
)

# Include all API endpoints
app.include_router(
    insurance.router,
    prefix="/api/v1",
    tags=["Insurance Calculations"],
    responses={
        400: {"description": "Invalid input parameters"},
        500: {"description": "Internal server error"}
    }
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
