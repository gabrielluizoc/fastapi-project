"""
Insurance calculation API endpoints.
Defines the REST interface for insurance premium calculations.
"""

from decimal import Decimal
from fastapi import APIRouter, Depends
from src.application.dtos.insurance_dto import InsuranceInputDto
from src.application.use_cases.insurance import CalculateInsuranceUseCase
from src.domain.entities.car import Car
from src.domain.value_objects.money import Money
from src.domain.value_objects.percentage import Percentage
from src.interfaces.schemas.insurance import InsuranceRequest, InsuranceResponse

router = APIRouter(
    prefix="/insurance",
    tags=["Insurance Calculations"],
    responses={
        400: {"description": "Invalid input parameters"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)

@router.post(
    "/calculate",
    response_model=InsuranceResponse,
    summary="Calculate insurance premium",
    description="""
    Calculates the insurance premium based on vehicle details and coverage parameters.
    
    Performs the following calculations:
    - Determines dynamic rate based on car age and value
    - Applies deductible percentage
    - Includes broker fee in final premium
    - Calculates policy limits
    """,
    response_description="Insurance calculation results",
    openapi_extra={
        "examples": {
            "standard": {
                "summary": "Standard calculation",
                "value": {
                    "make": "Toyota",
                    "model": "Corolla",
                    "year": 2012,
                    "value": 100000.00,
                    "deductible_percentage": 0.1,
                    "broker_fee": 50.00
                }
            },
            "luxury": {
                "summary": "Luxury vehicle",
                "value": {
                    "make": "BMW",
                    "model": "X5",
                    "year": 2022,
                    "value": 75000.00,
                    "deductible_percentage": 0.2,
                    "broker_fee": 100.00
                }
            }
        }
    }
)
async def calculate(
        request: InsuranceRequest,
        use_case: CalculateInsuranceUseCase = Depends()
) -> InsuranceResponse:
    """
    Calculate insurance premium endpoint.

    Transforms API request into domain objects, executes business logic,
    and formats the response for the client.

    Args:
        request: InsuranceRequest containing:
            - make: Vehicle manufacturer
            - model: Vehicle model
            - year: Manufacturing year
            - value: Vehicle value (decimal)
            - deductible_percentage: Deductible rate (0-1)
            - broker_fee: Broker commission fee

        use_case: Injected CalculateInsuranceUseCase instance

    Returns:
        InsuranceResponse containing:
            - applied_rate: Formatted percentage string
            - calculated_premium: Formatted monetary value
            - policy_limit: Formatted monetary value
            - deductible_value: Formatted monetary value

    Raises:
        HTTPException:
            - 400: If business validation fails
            - 422: If input data validation fails
            - 500: For unexpected server errors

    Example:
        POST /insurance/calculate
        {
            "make": "Honda",
            "model": "Civic",
            "year": 2019,
            "value": 20000.00,
            "deductible_percentage": 0.15,
            "broker_fee": 75.00
        }
    """
    # Convert API request to domain entities
    car = Car(
        make=request.make,
        model=request.model,
        year=request.year,
        value=Money(Decimal(str(request.value))),
        deductible_percentage=Percentage(Decimal(str(request.deductible_percentage)))
    )

    # Prepare use case input
    _input = InsuranceInputDto(
        car=car,
        broker_fee=Money(Decimal(str(request.broker_fee)))
    )

    # Execute business logic
    output = use_case.execute(_input)

    # Format domain output for API response
    return InsuranceResponse(
        applied_rate=f"{output.applied_rate.value * 100:.2f}%",
        calculated_premium=str(output.calculated_premium),
        policy_limit=str(output.policy_limit),
        deductible_value=str(output.deductible_value)
    )
