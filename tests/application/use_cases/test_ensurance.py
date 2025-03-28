import pytest
from decimal import Decimal
from unittest.mock import Mock
from src.application.use_cases.insurance import CalculateInsuranceUseCase
from src.domain.entities.car import Car
from src.domain.value_objects.money import Money
from src.domain.value_objects.percentage import Percentage

class TestCalculateInsuranceUseCase:
    @pytest.fixture
    def test_car(self):
        return Car(
            make="Toyota",
            model="Corolla",
            year=2020,
            value=Money(Decimal("30000.00")),
            deductible_percentage=Percentage(Decimal("0.1"))
        )

    def test_premium_calculation(self, test_car):
        use_case = CalculateInsuranceUseCase()
        input_dto = Mock()
        input_dto.car = test_car
        input_dto.broker_fee = Money(Decimal("50.00"))

        result = use_case.execute(input_dto)

        assert isinstance(result.applied_rate, Percentage)
        assert isinstance(result.calculated_premium, Money)
        assert result.calculated_premium.amount > Decimal("0")
