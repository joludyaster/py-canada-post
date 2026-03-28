from functools import wraps
import xmltodict

from ..exceptions.exception_map import ERROR_MAP

CODE = "code"
MESSAGE = "message"
MESSAGES = "messages"

def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        parsed_response = xmltodict.parse(response.text)
        code = parsed_response.get(MESSAGES, {}).get(MESSAGE, {}).get(CODE)

        error_map = ERROR_MAP.get(code, None)

        if not error_map:
            return response

        error_exception = error_map.exception
        error_description = error_map.description
        error_mitigation = error_map.mitigation

        raise error_exception(error_description, error_mitigation)

    return wrapper