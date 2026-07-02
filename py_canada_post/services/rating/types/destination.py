from dataclasses import dataclass


@dataclass
class DomesticDestination:
    postal_code: str
    """
    Postal code.

    Format ANANAN (only accepted with uppercase).
    """


@dataclass
class UnitedStatesDestination:
    zip_code: str
    """
    Zip code.

    Used when country code = US. Format is 5 digits or 5-4 (for extended Zip Codes).

    E.g. 12345 or 12345-6789.
    """


@dataclass
class InternationalDestination:
    country_code: str
    """
    Country code.

    The destination country code. 
    Standard 2-character country code (valid country code other than CA or US).
    """
    postal_code: str
    """
    Postal code.

    The Postal Code field can be provided if the customer would like 
    to receive a Guaranteed date for a Kahala Posts Group (KPG) country.
    """


@dataclass
class Destination:
    domestic: DomesticDestination | None = None
    """
    Domestic.
    """
    united_states: UnitedStatesDestination | None = None
    """
    United states.
    """
    international: InternationalDestination | None = None
    """
    International.
    """
