"""
Data Transfer Objects (DTOs) for insurance premium calculation.
These classes define the input/output data structures for the insurance use case.
"""
from dataclasses import dataclass
from src.domain.entities.car import Car
from src.domain.value_objects.money import Money
from src.domain.value_objects.percentage import Percentage


@dataclass
class InsuranceInputDto:
    """
    Input data structure for insurance premium calculation.

    Attributes:
        car (Car): The car entity containing vehicle details for insurance calculation.
        broker_fee (Money): The broker's fee to be included in premium calculation.

    Example:
        >>> from decimal import Decimal
        >>> input_dto = InsuranceInputDto(
        ...     car=Car(make="Toyota", model="Corolla", ...),
        ...     broker_fee=Money(Decimal("50.00"))
        ... )
    """
    car: Car
    broker_fee: Money

@dataclass
class InsuranceOutputDto:
    """
    Output data structure containing insurance calculation results.

    Attributes:
        applied_rate (Percentage): The final insurance rate applied to the premium.
        calculated_premium (Money): The total insurance premium after calculations.
        policy_limit (Money): The maximum coverage amount for the policy.
        deductible_value (Money): The deductible amount to be paid by the insured.

    Example:
        >>> from decimal import Decimal
        >>> output_dto = InsuranceOutputDto(
        ...     applied_rate=Percentage(Decimal("0.1")),
        ...     calculated_premium=Money(Decimal("1200.00")),
        ...     policy_limit=Money(Decimal("10000.00")),
        ...     deductible_value=Money(Decimal("500.00"))
        ... )
    """
    applied_rate: Percentage
    calculated_premium: Money
    policy_limit: Money
    deductible_value: Money
