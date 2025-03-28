import pytest
from decimal import Decimal
from src.domain.value_objects.money import Money

class TestMoney:
    def test_create_valid_money(self):
        money = Money(Decimal("100.50"))
        assert money.amount == Decimal("100.50")
        assert money.currency == "USD"

    def test_negative_amount_raises_error(self):
        with pytest.raises(ValueError):
            Money(Decimal("-100"))

    def test_non_decimal_raises_error(self):
        with pytest.raises(TypeError):
            Money(100.50)  # float instead of Decimal

    def test_repr_representation(self):
        money = Money(Decimal("1500.75"))
        assert repr(money) == "USD 1,500.75"
