import xmltodict
from requests import Response


class ResponseToObject:
    def __init__(self, response: Response):
        self.response = response
        self.parsed_response = xmltodict.parse(response.text)