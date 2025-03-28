"""
Value object representing monetary amounts with currency support.
Provides type safety and basic validation for financial calculations.
"""

from decimal import Decimal

from src.config import Config


class Money:
    """
    Immutable value object representing a monetary amount with currency.

    Enforces:
    - Decimal precision for financial calculations
    - Non-negative values
    - Type safety for amounts
    - Currency formatting (default: USD)

    Args:
        amount (Decimal): The monetary value as a Decimal for precision
        currency (str): ISO currency code (default: "USD")

    Raises:
        TypeError: If amount is not a Decimal
        ValueError: If amount is negative

    Example:
        >>> money = Money(Decimal("1000.50"))
        >>> print(money)
        USD 1,000.50
        >>> money.amount
        Decimal('1000.50')
    """
    def __init__(self, amount: Decimal, currency: str = Config.DEFAULT_CURRENCY):
        """
        Initialize a Money instance with validation.

        Args:
            amount: Monetary value as Decimal for precise calculations
            currency: ISO currency code (default: "USD" from config file)

        Raises:
            TypeError: If amount is not a Decimal type
            ValueError: If amount is negative
        """
        if not isinstance(amount, Decimal):
            raise TypeError("Amount must be a Decimal.")
        if amount < Decimal("0"):
            raise ValueError("Amount cannot be negative.")
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        """
       Machine-readable string representation of Money object.

       Returns:
           str: Format "CURRENCY AMOUNT" (e.g., "USD 1,000.50")

       Example:
           >>> repr(Money(Decimal("1500.75")))
           'USD 1,500.75'
       """
        return f"{self.currency} {self.amount:,.2f}"
