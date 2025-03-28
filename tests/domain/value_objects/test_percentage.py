import pytest
from decimal import Decimal
from src.domain.value_objects.percentage import Percentage

class TestPercentage:
    def test_valid_percentage(self):
        pct = Percentage(Decimal("0.15"))
        assert pct.value == Decimal("0.15")

    def test_out_of_range_raises_error(self):
        with pytest.raises(ValueError):
            Percentage(Decimal("1.5"))

        with pytest.raises(ValueError):
            Percentage(Decimal("-0.1"))

    def test_repr_representation(self):
        pct = Percentage(Decimal("0.255"))
        assert repr(pct) == "25.50%"

    def test_percentage_requires_decimal(self):
        invalid_types = [
            0.5,
            "0.5",
            1,
            True,
            None
        ]

        for invalid_value in invalid_types:
            with pytest.raises(TypeError) as excinfo:
                Percentage(invalid_value)
            assert "Percentage must be initialized with Decimal" in str(excinfo.value)