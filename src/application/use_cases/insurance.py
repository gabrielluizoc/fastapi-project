"""
Insurance premium calculation business logic.
Contains the core algorithm for determining insurance rates and premiums.
"""

from decimal import Decimal
from src.config import Config
from src.domain.value_objects.money import Money
from src.domain.value_objects.percentage import Percentage
from src.application.dtos.insurance_dto import InsuranceInputDto, InsuranceOutputDto

class CalculateInsuranceUseCase:
    """
    Handles the insurance premium calculation business logic.

    This use case:
    - Calculates dynamic rates based on car age and value
    - Determines base premium and final premium after deductible
    - Computes policy limits and deductible values
    - Uses application-wide configuration for rates

    The calculation follows the formula:
    Final Premium = (Car Value × Applied Rate) - Deductible + Broker Fee
    """

    @staticmethod
    def execute(_input: InsuranceInputDto) -> InsuranceOutputDto:
        """
        Execute the insurance premium calculation.

        Args:
            _input: InsuranceInputDto containing:
                - car: Car entity with vehicle details
                - broker_fee: Broker's commission fee

        Returns:
            InsuranceOutputDto containing:
                - applied_rate: Calculated insurance rate (Percentage)
                - calculated_premium: Final premium amount (Money)
                - policy_limit: Maximum coverage amount (Money)
                - deductible_value: Deductible amount (Money)

        Calculation Steps:
        1. Rate Calculation:
           - Age Rate: base_rate × car_age
           - Value Rate: base_rate × (car_value / $10,000)
           - Applied Rate = Age Rate + Value Rate

        2. Premium Calculation:
           - Base Premium = car_value × applied_rate
           - Deductible Discount = base_premium × deductible_percentage
           - Final Premium = base_premium - deductible_discount + broker_fee

        3. Policy Limit Calculation:
           - Base Limit = car_value × coverage_percentage
           - Deductible Value = base_limit × deductible_percentage
           - Final Limit = base_limit - deductible_value

        Example:
            >>> from decimal import Decimal
            >>> from src.domain.entities.car import Car
            >>> car = Car(...)
            >>> input_dto = InsuranceInputDto(car=car, broker_fee=Money(Decimal("50"))
            >>> output = CalculateInsuranceUseCase.execute(input_dto)
            >>> output.calculated_premium
            Money('USD 1200.00')
        """
        # 1. Rate Calculation
        age_rate = Config.INSURANCE_BASE_RATE * _input.car.get_age()
        value_rate = Config.INSURANCE_BASE_RATE * (_input.car.value.amount / Decimal("10000"))
        applied_rate = age_rate + value_rate

        # 2. Premium Calculation
        base_premium = _input.car.value.amount * applied_rate
        deductible_discount = base_premium * _input.car.deductible_percentage.value
        final_premium = Money(base_premium - deductible_discount + _input.broker_fee.amount)

        # 3. Policy Limit Calculation
        base_policy_limit = _input.car.value.amount * Config.INSURANCE_COVERAGE_PERCENTAGE
        deductible_value = base_policy_limit * _input.car.deductible_percentage.value
        final_policy_limit = Money(base_policy_limit - deductible_value)

        return InsuranceOutputDto(
            applied_rate=Percentage(applied_rate),
            calculated_premium=final_premium,
            policy_limit=final_policy_limit,
            deductible_value=Money(deductible_value)
        )
