from datetime import datetime
from typing import TypeVar, Type, Iterable, Any

import xmltodict
from requests import Response

T = TypeVar("T")
KeyPath = str | Iterable[str] | None


def transform_date(date: str) -> datetime | None:
    """
    Function to transform date.

    Parameters
    ----------
    date : str
        Potential date to be transformed.

    Returns
    -------
    datetime or None
        Either a valid datetime or None.
    """

    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return None


def is_float(value: str) -> bool:
    """
    Function to check if the string is a valid float or if it's possible to convert it to float.

    Parameters
    ----------
    value : str
        Value to be transformed into the float.

    Returns
    -------
    bool
        True if it's possible to convert a string into the float, False otherwise.
    """

    try:
        float(value)
        return True
    except ValueError:
        return False


class ResponseToObject:
    def __init__(self, response: Response) -> None:
        """
        Initialize class variables.

        Parameters
        ----------
        response : Response
            Response object.
        """

        self.response = response
        self.parsed_response = xmltodict.parse(response.text)

    @staticmethod
    def _get_objects(obj: dict, keys: list[str]) -> Any | None:
        """
        Function to get the specific data based on the keys provided.

        Parameters
        ----------
        obj : dict
            Dictionary object to search through.
        keys : list[str]
            Keys to use in order to get the specific data.

        Examples
        ----------
        >>> test = {
        >>>    "something cool": {
        >>>        "another cool": {
        >>>            "here we are": 1
        >>>        }
        >>>    }
        >>> }
        >>> ResponseToObject()._get_objects(obj=test, keys=["something cool", "another cool"]) # {"here we are": 1}

        Returns
        -------
        Any | None
            Either a list of dictionaries or a dictionary itself or None.
        """

        current = obj

        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
            else:
                return None

            if current is None:
                return None

        return current

    @staticmethod
    def _get_nested_value(obj: dict, path: KeyPath) -> Any | None:
        """
        Function to either get an object if the path is a single value or loop through the path keys and get the value.

        Parameters
        ----------
        obj : dict
            Dictionary object to search through.
        path : KeyPath
            Either a string or a tuple of string.

        Examples
        ----------
        >>> d = {
        >>>    "something cool": 2,
        >>>    "nested": {
        >>>        "here we are": 3
        >>>    }
        >>> }
        >>> ResponseToObject()._get_nested_value(obj=d, path=("nested", "here we are"))

        Returns
        -------
        Any
            An object from dictionary.
        """

        if isinstance(path, str):
            return obj.get(path, None)

        if path is None:
            return None

        current = obj
        for key in path:
            try:
                current = current.get(key)
            except (AttributeError, KeyError):
                return None

        return current

    def _construct_object(self, obj: dict, keys: list[KeyPath], cls: Type[T]) -> T:
        """
        Function to construct a dataclass-type object with value by unpacking a list of data.

        Parameters
        ----------
        obj : dict
            Dictionary where the data will be extracted from.
        keys : list[KeyPath]
            List of keys to search for in a dictionary.
        cls : Type[TypeVar("T")]
            Dataclass-type object.

        Returns
        -------
        T
            Dataclass.
        """

        data = []

        for key in keys:
            nested_key = self._get_nested_value(obj, key)

            if nested_key in ("true", "false"):
                data.append(nested_key == "true")

            elif isinstance(nested_key, str) and nested_key.isdigit():
                data.append(int(nested_key))

            elif isinstance(nested_key, str) and is_float(nested_key):
                data.append(float(nested_key))

            elif isinstance(nested_key, str) and transform_date(nested_key):
                data.append(transform_date(nested_key))

            else:
                data.append(nested_key)

        return cls(*data)

    def _construct_objects(self, obj: dict, search_keys: list[KeyPath], obj_keys: list[KeyPath], cls: Type[T]) -> list[
                                                                                                                      T] | None:
        """
        Function to construct a list of dataclass-type objects with data.

        Parameters
        ----------
        obj : dict
            Dictionary where the data will be extracted from.
        search_keys : list[KeyPath]
            List of keys to get a specific object.
        obj_keys : list[KeyPath]
            List of keys to get detailed information about the object.
        cls : Type[TypeVar("T")]
            Dataclass-type object.

        Returns
        -------
        list[Type[TypeVar("T")]] or None
            Either a list of dataclasses or None.
        """

        objects = self._get_objects(obj, search_keys)

        if isinstance(objects, list):
            return [self._construct_object(object, obj_keys, cls) for object in objects]

        if isinstance(objects, dict):
            return [self._construct_object(objects, obj_keys, cls)]

        return None
