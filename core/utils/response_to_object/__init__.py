import datetime
from typing import Optional, Union, TypeVar, Type, Iterable

import xmltodict
from requests import Response
from datetime import datetime

T = TypeVar("T")
KeyPath = Union[str, Iterable[str]]

def is_date_valid(date: str) -> Optional[datetime]:
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return None

def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False

class ResponseToObject:
    def __init__(self, response: Response):
        self.response = response
        self.parsed_response = xmltodict.parse(response.text)

    @staticmethod
    def _get_objects(obj: dict, keys: list[str]) -> Optional[Union[dict, list]]:
        """
        Function to get the specific data based on the keys provided

        Parameters
        ----------
        obj : dict
            Dictionary object to search through
        keys : list[str]
            Keys to use in order to get the specific data

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
        Optional[Union[dict, list]]
            Either a list of dictionaries or a dictionary itself
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
    def _get_nested_value(obj: dict, path: KeyPath) -> str:
        """
        Function to either get an object if the path is a single value or loop through the path keys and get the value

        Parameters
        ----------
        obj : dict
            Dictionary object to search through
        path : KeyPath
            Either a string or a tuple of string


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
        str
            An object from dictionary
        """
        if isinstance(path, str):
            return obj[path]

        current = obj
        for key in path:
            current = current[key]
        return current

    def _construct_object(self, obj: dict, keys: list[KeyPath], cls: Type[T]) -> T:
        """
        Function to construct a dataclass-type object with value by unpacking a list of data

        Parameters
        ----------
        obj : dict
            Dictionary where the data will be extracted from
        keys : list[KeyPath]
            List of keys to search for in a dictionary
        cls : Type[TypeVar("T")]
            Dataclass-type object

        Returns
        -------
        T
            Dataclass
        """
        data = []

        for key in keys:
            nested_key = self._get_nested_value(obj=obj, path=key)

            if nested_key in ("true", "false"):
                data.append(nested_key == "true")
            elif nested_key.isdigit():
                data.append(int(nested_key))
            elif is_float(value=nested_key):
                data.append(float(nested_key))
            elif is_date_valid(date=nested_key):
                data.append(is_date_valid(date=nested_key))
            else:
                data.append(nested_key)

        return cls(*data)

    def _construct_objects(self, obj: dict, search_keys: list[KeyPath], obj_keys: list[KeyPath], cls: Type[T]) -> Optional[list[T]]:
        """
        Function to construct a list of dataclass-type objects with data

        Parameters
        ----------
        obj : dict
            Dictionary where the data will be extracted from
        search_keys : list[KeyPath]
            List of keys to get a specific object
        obj_keys : list[KeyPath]
            List of keys to get detailed information about the object
        cls : Type[TypeVar("T")]
            Dataclass-type object

        Returns
        -------
        Optional[list[Type[TypeVar("T")]]]
            Either a list of dataclasses or None
        """
        objects = self._get_objects(obj=obj, keys=search_keys)

        if not objects:
            return None

        if isinstance(objects, list):
            return [self._construct_object(obj=object, keys=obj_keys, cls=cls) for object in objects]

        return [self._construct_object(obj=objects, keys=obj_keys, cls=cls)]