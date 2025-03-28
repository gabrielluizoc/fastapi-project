import pytest
from decimal import Decimal
from src.domain.entities.car import Car
from src.interfaces.schemas.insurance import InsuranceRequest, InsuranceResponse

class TestInsuranceSchemas:
    def test_request_valid_data(self):
        request = InsuranceRequest(
            make="Toyota",
            model="Corolla",
            year=2020,
            value=Decimal("35000.00"),
            deductible_percentage=Decimal("0.1"),
            broker_fee=Decimal("50.00")
        )
        assert request.make == "Toyota"

    def test_request_invalid_year(self):
        with pytest.raises(ValueError):
            InsuranceRequest(
                make="Toyota",
                model="Corolla",
                year=2050,
                value=Decimal("35000.00"),
                deductible_percentage=Decimal("0.1"),
                broker_fee=Decimal("50.00")
            )

    def test_response_schema(self):
        response = InsuranceResponse(
            applied_rate="5.50%",
            calculated_premium="USD 1,200.00",
            policy_limit="USD 30,000.00",
            deductible_value="USD 500.00"
        )
        assert response.calculated_premium.startswith("USD")

    def test_to_entity_conversion(self):
        request = InsuranceRequest(
            make="Toyota",
            model="Corolla",
            year=2012,
            value=Decimal("100000.00"),
            deductible_percentage=Decimal("0.1"),
            broker_fee=Decimal("50.00")
        )

        car = request.to_entity()

        assert isinstance(car, Car)
        assert car.make == "Toyota"
        assert car.model == "Corolla"
        assert car.year == 2012
        assert car.value.amount == Decimal("100000.00")
        assert car.deductible_percentage.value == Decimal("0.1")
