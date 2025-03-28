"""
Pydantic schemas for insurance API requests and responses.
Defines the data contracts for the insurance calculation endpoint.
"""

from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field
from src.domain.entities.car import Car
from src.domain.value_objects.money import Money
from src.domain.value_objects.percentage import Percentage

class InsuranceRequest(BaseModel):
    """
    Request schema for insurance premium calculation.

    Attributes:
        make (str): Vehicle manufacturer (e.g., "Toyota")
        model (str): Vehicle model (e.g., "Corolla")
        year (int): Manufacturing year (must be ≤ current year)
        value (Decimal): Current market value (must be positive)
        deductible_percentage (Decimal): Deductible rate (0.0-1.0 range)
        broker_fee (Decimal): Broker commission fee (must be ≥ 0)

    Examples:
        >>> request = InsuranceRequest(
        ...     make="Honda",
        ...     model="Civic",
        ...     year=2020,
        ...     value=Decimal("25000.00"),
        ...     deductible_percentage=Decimal("0.1"),
        ...     broker_fee=Decimal("50.00")
        ... )
    """

    make: str = Field(
        ...,
        example="Toyota",
        description="Manufacturer of the vehicle",
        min_length=2,
        max_length=50
    )
    model: str = Field(
        ...,
        example="Corolla",
        description="Model name of the vehicle",
        min_length=1,
        max_length=50
    )
    year: int = Field(
        ...,
        example=2012,
        description="Manufacturing year of the vehicle",
        ge=1900,
        le=datetime.now().year
    )
    value: Decimal = Field(
        ...,
        example=100000.00,
        description="Current market value of the vehicle",
        gt=0,
        max_digits=12,
        decimal_places=2
    )
    deductible_percentage: Decimal = Field(
        ...,
        example=0.1,
        description="Deductible rate (0.0 = 0%, 1.0 = 100%)",
        ge=0,
        le=1,
        max_digits=3,
        decimal_places=2
    )
    broker_fee: Decimal = Field(
        ...,
        example=50.00,
        description="Broker commission fee amount",
        ge=0,
        max_digits=10,
        decimal_places=2
    )

    def to_entity(self) -> Car:
        """
        Convert the request schema to a domain entity.

        Returns:
            Car: Initialized Car entity with validated values

        Example:
            >>> request = InsuranceRequest(
            ...     make="Toyota",
            ...     model="Corolla",
            ...     year=2012,
            ...     value=Decimal("100000.00"),
            ...     deductible_percentage=Decimal("0.1"),
            ...     broker_fee=Decimal("50.00")
            ... )
            >>> car = request.to_entity()
            >>> isinstance(car, Car)
            True
        """
        return Car(
            make=self.make,
            model=self.model,
            year=self.year,
            value=Money(self.value),
            deductible_percentage=Percentage(self.deductible_percentage)
        )

    class Config:
        """
        Pydantic model configuration for InsuranceRequest.

        Attributes:
            json_schema_extra (dict): Example schema for OpenAPI documentation.
        """
        json_schema_extra = {
            "example": {
                "make": "Toyota",
                "model": "Corolla",
                "year": 2012,
                "value": 100000.00,
                "deductible_percentage": 0.1,
                "broker_fee": 50.00
            }
        }


class InsuranceResponse(BaseModel):
    """
    Response schema for insurance calculation results.

    Attributes:
        applied_rate (str): Formatted insurance rate (e.g., "5.50%")
        calculated_premium (str): Formatted premium amount (e.g., "USD 1,200.00")
        policy_limit (str): Formatted coverage limit (e.g., "USD 30,000.00")
        deductible_value (str): Formatted deductible amount (e.g., "USD 500.00")

    Examples:
        >>> response = InsuranceResponse(
        ...     applied_rate="5.50%",
        ...     calculated_premium="USD 1,200.00",
        ...     policy_limit="USD 30,000.00",
        ...     deductible_value="USD 500.00"
        ... )
    """

    applied_rate: str = Field(
        ...,
        example="5.50%",
        description="Calculated insurance rate as percentage"
    )
    calculated_premium: str = Field(
        ...,
        example="USD 1,200.00",
        description="Final premium amount with currency"
    )
    policy_limit: str = Field(
        ...,
        example="USD 30,000.00",
        description="Maximum coverage amount with currency"
    )
    deductible_value: str = Field(
        ...,
        example="USD 500.00",
        description="Deductible amount with currency"
    )

    class Config:
        """
        Pydantic model configuration for InsuranceResponse.

        Attributes:
            json_schema_extra (dict): Example schema for OpenAPI documentation.
        """
        json_schema_extra = {
            "example": {
                "applied_rate": "5.50%",
                "calculated_premium": "USD 1,200.00",
                "policy_limit": "USD 30,000.00",
                "deductible_value": "USD 500.00"
            }
        }
