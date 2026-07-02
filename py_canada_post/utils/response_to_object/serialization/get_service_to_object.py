from typing import Any

from requests import Response

from py_canada_post.services.rating.types import Service
from py_canada_post.utils.response_to_object.serialization.rate_to_object import ResponseToObject
from py_canada_post.services.rating.types import Option, Restrictions, AttributeRestriction, DimensionalRestrictions

SERVICE = "service"

SERVICE_NAME = "service-name"
SERVICE_CODE = "service-code"
COMMENT = "comment"

OPTIONS = "options"
OPTION = "option"
OPTION_CODE = "option-code"
OPTION_NAME = "option-name"
MANDATORY = "mandatory"
QUALIFIER_REQUIRED = "qualifier-required"
QUALIFIER_MAX = "qualifier-max"

RESTRICTIONS = "restrictions"
WEIGHT_RESTRICTION = "weight-restriction"
DIMENSIONAL_RESTRICTIONS = "dimensional-restrictions"
LENGTH = "length"
WIDTH = "width"
HEIGHT = "height"
MIN = "@min"
MAX = "@max"
LENGTH_PLUS_GIRTH_MAX = "length-plus-girth-max"
LENGTH_HEIGHT_WIDTH_SUM_MAX = "length-height-width-sum-max"
OVERSIZE_LIMIT = "oversize-limit"

DENSITY_FACTOR = "density-factor"
CAN_SHIP_IN_MAILING_TUBE = "can-ship-in-mailing-tube"
CAN_SHIP_UNPACKAGED = "can-ship-unpackaged"
ALLOWED_AS_RETURN_SERVICE = "allowed-as-return-service"

class GetServiceToObject(ResponseToObject):
    def __init__(self, response: Response) -> None:
        """
        Initialize class variables.

        Parameters
        ----------
        response : Response
            Response object.
        """

        super().__init__(response)

    def response_to_object(self) -> Service | None:
        """
        Main function to deserialize xml response object.

        Returns
        -------
        Service or None
            Service or None.
        """

        return self._construct_service(self.parsed_response)

    def _construct_options(self, obj: dict) -> list[Option] | None:
        """
        Function to construct options.

        Parameters
        ----------
        obj : dict
            Object dictionary.

        Returns
        -------
        list[Option] or None
            Either a list of option(s) or None.
        """

        return self._construct_objects(
            obj,
            [SERVICE, OPTIONS, OPTION],
            [OPTION_CODE, None, None, None, OPTION_NAME, MANDATORY, QUALIFIER_REQUIRED, QUALIFIER_MAX],
            Option
        )

    def _construct_attribute_restriction(self, obj: dict, obj_keys: list[Any], search_keys: list[Any] = None) -> AttributeRestriction:
        """
        Function to construct reusable attribute restriction based on object keys and search keys.

        Parameters
        ----------
        obj : dict
            Object dictionary.
        obj_keys : list[Any]
            A list of keys -> could be a list of just the strings or a tuple of strings (e.g. (SERVICE, RESTRICTIONS)).
        search_keys : list[Any], optional
            A list of search keys that are used to search for a specific object first before using the object keys to search through.

        Returns
        -------
        AttributeRestriction
        """
        s_keys = search_keys if search_keys else [SERVICE, RESTRICTIONS]
        keys = [(*s_keys, *o_keys) for o_keys in obj_keys]

        return self._construct_object(
            obj,
            keys,
            AttributeRestriction
        )

    def _construct_dimensional_restriction(self, obj: dict, key: str) -> AttributeRestriction:
        """
        Function to construct reusable dimensional restriction.

        Parameters
        ----------
        obj : dict
            Object dictionary.
        key : str
            Key string that is used to call self._construct_attribute_restriction() to create a reusable attribute restriction.

        Returns
        -------
        AttributeRestriction
        """
        return self._construct_attribute_restriction(
            obj,
            [(key, MIN), (key, MAX)],
            [SERVICE, RESTRICTIONS, DIMENSIONAL_RESTRICTIONS]
        )

    def _construct_restrictions(self, obj: dict) -> Restrictions | None:
        """
        Function to construct restrictions object.

        Parameters
        ----------
        obj : dict
            Object dictionary.

        Returns
        -------
        Restrictions or None
            Either a restrictions object or None.
        """
        r_obj = self._get_objects(obj, [SERVICE, RESTRICTIONS, DIMENSIONAL_RESTRICTIONS])

        if not r_obj:
            return None

        weight_restriction = self._construct_attribute_restriction(
            obj,
            [(WEIGHT_RESTRICTION, MIN), (WEIGHT_RESTRICTION, MAX)]
        )
        dimensional_length_restriction = self._construct_dimensional_restriction(obj, LENGTH)
        dimensional_width_restriction = self._construct_dimensional_restriction(obj, WIDTH)
        dimensional_height_restriction = self._construct_dimensional_restriction(obj, HEIGHT)

        length_plus_girth_max = r_obj.get(LENGTH_PLUS_GIRTH_MAX)
        length_height_width_sum_max = r_obj.get(LENGTH_HEIGHT_WIDTH_SUM_MAX)
        oversize_limit = r_obj.get(OVERSIZE_LIMIT)

        dimensional_restrictions = DimensionalRestrictions(
            length=dimensional_length_restriction,
            width=dimensional_width_restriction,
            height=dimensional_height_restriction,
            length_plus_girth_max=int(length_plus_girth_max),
            length_height_width_sum_max=length_height_width_sum_max,
            oversize_limit=int(oversize_limit)
        )

        restrictions = self._construct_object(
            obj,
            [None, None, *[(SERVICE, RESTRICTIONS, key) for key in [DENSITY_FACTOR, CAN_SHIP_IN_MAILING_TUBE, CAN_SHIP_UNPACKAGED, ALLOWED_AS_RETURN_SERVICE]]],
            Restrictions
        )

        if not restrictions:
            return None

        restrictions.weight_restriction = weight_restriction
        restrictions.dimensional_restrictions = dimensional_restrictions

        return restrictions

    def _construct_service(self, obj: dict) -> Service | None:
        """
        Function to construct service.

        Parameters
        ----------
        obj : dict
            Object dictionary.

        Returns
        -------
        Service or None
            Service or None
        """

        service_code = obj.get(SERVICE).get(SERVICE_CODE)
        service_name = obj.get(SERVICE, {}).get(SERVICE_NAME)
        comment = obj.get(SERVICE, {}).get(COMMENT)
        options = self._construct_options(obj)
        restrictions = self._construct_restrictions(obj)

        return Service(
            service_code=service_code,
            service_name=service_name,
            comment=comment,
            options=options,
            restrictions=restrictions
        )
