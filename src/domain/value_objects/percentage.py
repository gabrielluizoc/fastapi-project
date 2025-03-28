"""
Value object representing a percentage with strict validation.
Ensures percentage values are always within standard bounds (0%-100%).
"""

from decimal import Decimal

class Percentage:
    """
    Immutable percentage value object with decimal precision.

    Represents a percentage value between 0% and 100% (0.0 to 1.0 in decimal form).
    Enforces type safety and valid range constraints.

    Args:
        value (Decimal): Percentage value as decimal (0.0-1.0 range)

    Raises:
        TypeError: If value is not a Decimal
        ValueError: If value is outside 0-1 range

    Example:
        >>> discount = Percentage(Decimal("0.15"))  # 15% discount
        >>> print(discount)
        15.00%
        >>> tax = Percentage(Decimal("0.075"))  # 7.5% tax
        >>> tax.value
        Decimal('0.075')
    """

    def __init__(self, value: Decimal):
        """
        Initialize a Percentage with validation.

        Args:
            value: Percentage value as Decimal (must be 0.0 ≤ value ≤ 1.0)

        Raises:
            TypeError: If input is not a Decimal
            ValueError: If value is outside valid range
        """
        if not isinstance(value, Decimal):
            raise TypeError("Percentage must be initialized with Decimal")
        if not Decimal("0") <= value <= Decimal("1"):
            raise ValueError("Percentage must be between 0 and 1 (0% to 100%)")
        self.value = value

    def __repr__(self) -> str:
        """
        String representation showing formatted percentage.

        Returns:
            str: Formatted percentage with 2 decimal places and % sign

        Example:
            >>> repr(Percentage(Decimal("0.255")))
            '25.50%'
        """
        return f"{self.value * Decimal('100'):.2f}%"
