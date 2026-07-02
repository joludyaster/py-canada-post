from dataclasses import dataclass


@dataclass
class Dimensions:
    length: float
    """
    Length in cm.

    Longest dimension.

    (3.1 digits e.g. 999.9 pattern).
    """
    width: float
    """
    Width in cm.

    Second longest dimension.

    (3.1 digits e.g. 999.9 pattern).
    """
    height: float
    """
    Height in cm.

    Shortest dimension.

    (3.1 digits e.g. 999.9 pattern).
    """


@dataclass
class ParcelCharacteristics:
    weight: float
    """
    Weight in kg.

    The weight of the parcel in kilograms.

    (99.999)
    """
    dimensions: Dimensions | None = None
    """
    Dimensions.
    """
