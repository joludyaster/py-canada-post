from dataclasses import is_dataclass
from datetime import datetime
from typing import Any
from xml.etree.ElementTree import Element


class ConstructXMLElement:

    def construct_xml_element(self, parent_tag: str, data: Any, child_tag: str = None) -> Element | None:
        if not data:
            return None

        element = None

        if not is_dataclass(data):
            if isinstance(data, list):
                if child_tag:
                    element = self._construct_from_list(parent_tag, child_tag, data)
            else:
                transformed_data = self._to_string(data)
                element = self._construct_from_string(parent_tag, transformed_data)
        else:
            element = self._construct_from_dataclass(parent_tag, data)

        return element

    @staticmethod
    def _construct_from_string(parent_tag: str, data: str) -> Element:
        element = Element(parent_tag)
        element.text = data
        return element

    def _construct_from_dataclass(self, parent_tag: str, obj: Any) -> Element | None:
        element = Element(parent_tag)

        filtered = {key: value for key, value in obj.__dict__.items() if value is not None}
        if not filtered:
            return None

        for key, value in filtered.items():
            if is_dataclass(value):
                child_element = self._construct_from_dataclass(key, value)
            else:
                child_element = Element(key.replace("_", "-"))
                child_element.text = str(value)

            if child_element is not None:
                element.append(child_element)

        return element

    def _construct_from_list(self, parent_tag: str, child_tag: str, data: list[Any]) -> Element | None:
        element = Element(parent_tag)

        if all(isinstance(item, str) for item in data):
            for item in data:
                child_element = self._construct_from_string(child_tag, item)
                element.append(child_element)

        elif all(is_dataclass(item) for item in data):
            for item in data:
                child_element = self._construct_from_dataclass(child_tag, item)
                if child_element is not None:
                    element.append(child_element)

        if len(element.findall(child_tag)) > 0:
            return element

        return None

    @staticmethod
    def _to_string(data: Any) -> str:
        to_string = str(data)
        if isinstance(data, float) or isinstance(data, int) or isinstance(data, bool):
            to_string = str(data).lower()

        elif isinstance(data, datetime):
            to_string = data.strftime("%Y-%m-%d")

        return to_string