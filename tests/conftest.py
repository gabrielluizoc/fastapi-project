import pytest
from decimal import Decimal
from src.domain.entities.car import Car
from src.domain.value_objects.money import Money
from src.domain.value_objects.percentage import Percentage

@pytest.fixture
def sample_car():
    return Car(
        make="Toyota",
        model="Corolla",
        year=2020,
        value=Money(Decimal("30000.00")),
        deductible_percentage=Percentage(Decimal("0.1"))
    )

@pytest.fixture
def sample_insurance_input(sample_car):
    return {
        "car": sample_car,
        "broker_fee": Money(Decimal("50.00"))
    }
