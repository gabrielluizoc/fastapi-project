import pytest
from decimal import Decimal
from datetime import datetime
from src.domain.entities.car import Car
from src.domain.value_objects.money import Money
from src.domain.value_objects.percentage import Percentage

class TestCar:
    @pytest.fixture
    def valid_car(self):
        return Car(
            make="Toyota",
            model="Corolla",
            year=2020,
            value=Money(Decimal("25000.00")),
            deductible_percentage=Percentage(Decimal("0.1"))
        )

    def test_valid_car_creation(self, valid_car):
        assert valid_car.make == "Toyota"
        assert valid_car.get_age() == (datetime.now().year - 2020)

    def test_future_year_raises_error(self):
        with pytest.raises(ValueError):
            Car(
                make="Tesla",
                model="Model S",
                year=2050,
                value=Money(Decimal("80000.00")),
                deductible_percentage=Percentage(Decimal("0.1"))
            )

    def test_negative_value_raises_error(self):
        with pytest.raises(ValueError):
            Car(
                make="Honda",
                model="Civic",
                year=2020,
                value=Money(Decimal("-10000.00")),
                deductible_percentage=Percentage(Decimal("0.1"))
            )
