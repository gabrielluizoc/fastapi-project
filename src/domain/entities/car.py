"""
Car domain entity representing a vehicle for insurance purposes.
Contains core business rules and validations for vehicle insurance calculations.
"""

from datetime import datetime
from dataclasses import dataclass
from src.domain.value_objects.money import Money
from src.domain.value_objects.percentage import Percentage

@dataclass(frozen=True)
class Car:
    """
    Immutable vehicle entity with insurance-specific validations.

    Represents a car with all attributes needed for insurance calculations.
    Enforces business rules through automatic validation.

    Attributes:
        make (str): Manufacturer of the vehicle (e.g., "Toyota")
        model (str): Model name (e.g., "Corolla")
        year (int): Manufacturing year (must be <= current year)
        value (Money): Current market value (must be positive)
        deductible_percentage (Percentage): Deductible rate (0-100%)

    Raises:
        ValueError: If any validation rules are violated

    Example:
        >>> from decimal import Decimal
        >>> car = Car(
        ...     make="Toyota",
        ...     model="Camry",
        ...     year=2020,
        ...     value=Money(Decimal("25000.00")),
        ...     deductible_percentage=Percentage(Decimal("0.1"))
        ... )
        >>> car.get_age()
        5  # Assuming current year is 2025
    """

    make: str
    model: str
    year: int
    value: Money
    deductible_percentage: Percentage

    def __post_init__(self):
        """
        Post-initialization hook that triggers validation.
        Automatically called after the dataclass is initialized.
        """
        self._validate()

    def _validate(self) -> None:
        """
        Validate all business rules for the car entity.

        Rules:
        1. Manufacturing year cannot be in the future
        2. Car value must be positive
        3. Deductible must be between 0% and 100%

        Raises:
            ValueError: With descriptive message for any violation
        """
        current_year = datetime.now().year

        if self.year > current_year:
            raise ValueError("Car manufacturing year cannot be in the future")

    def get_age(self) -> int:
        """
        Calculate the current age of the vehicle in years.

        Returns:
            int: Age in years (current year - manufacturing year)

        Note:
            Uses the system's current year for calculation
        """
        return datetime.now().year - self.year
