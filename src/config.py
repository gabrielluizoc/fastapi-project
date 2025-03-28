"""
Application configuration settings loaded from environment variables.
Provides centralized access to system configuration with default values.
"""
import os
from decimal import Decimal


class Config:
    """
    Centralized configuration management for insurance application.

    Loads settings from environment variables with fallback defaults.
    All monetary calculations use Decimal for precision.

    Class Attributes:
        DEFAULT_CURRENCY (str): Default currency code (ISO 4217 format).
            Environment var: DEFAULT_CURRENCY
            Default: "USD"

        INSURANCE_BASE_RATE (Decimal): Base insurance rate per unit calculation.
            Environment var: INSURANCE_BASE_RATE
            Default: Decimal("0.005") (0.5%)

        INSURANCE_COVERAGE_PERCENTAGE (Decimal): Default coverage percentage.
            Environment var: INSURANCE_COVERAGE_PERCENTAGE
            Default: Decimal("1.0") (100%)

    Example:
        >>> Config.DEFAULT_CURRENCY
        'USD'
        >>> Config.INSURANCE_BASE_RATE
        Decimal('0.005')
    """

    DEFAULT_CURRENCY = str(os.getenv("DEFAULT_CURRENCY", "USD"))
    """Default currency for all monetary values (ISO 4217 code)"""

    INSURANCE_BASE_RATE = Decimal(os.getenv("INSURANCE_BASE_RATE", "0.005"))
    """
    Base insurance rate used in premium calculations.
    
    Represents:
    - 0.5% per year for age-based calculation
    - 0.5% per $10,000 for value-based calculation
    """

    INSURANCE_COVERAGE_PERCENTAGE = Decimal(os.getenv("INSURANCE_COVERAGE_PERCENTAGE", "1.0"))
    """
    Default coverage percentage of vehicle value.
    
    Note:
        1.0 = 100% coverage
        0.8 = 80% coverage
    """

    @classmethod
    def validate(cls) -> None:
        """
        Validate configuration values at application startup.

        Raises:
            ValueError: If any configuration value fails validation
        """
        if not cls.DEFAULT_CURRENCY.isalpha() or len(cls.DEFAULT_CURRENCY) != 3:
            raise ValueError("DEFAULT_CURRENCY must be 3-letter ISO code")
        if cls.INSURANCE_BASE_RATE <= Decimal("0"):
            raise ValueError("INSURANCE_BASE_RATE must be positive")
        if not Decimal("0") < cls.INSURANCE_COVERAGE_PERCENTAGE <= Decimal("1"):
            raise ValueError("INSURANCE_COVERAGE_PERCENTAGE must be 0-1")
