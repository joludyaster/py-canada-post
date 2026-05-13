from functools import wraps

import xmltodict
from requests import Response

from py_canada_post.exceptions.exception_map import ERROR_MAP
from py_canada_post.exceptions.exceptions import ServerError

CODE = "code"
MESSAGE = "message"
DESCRIPTION = "description"
MESSAGES = "messages"


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        parsed_response = xmltodict.parse(response.text)
        code = parsed_response.get(MESSAGES, {}).get(MESSAGE, {}).get(CODE)
        code_description = parsed_response.get(MESSAGES, {}).get(MESSAGE, {}).get(DESCRIPTION)

        error_map = ERROR_MAP.get(code, None)

        if not error_map:
            return response

        error_exception = error_map.exception
        error_description = error_map.description

        if code_description and error_exception == ServerError:
            error_mitigation = code_description
        else:
            error_mitigation = error_map.mitigation

        raise error_exception(error_description, error_mitigation, response.status_code)

    return wrapper


@error_handler
def error_check(response: Response) -> Response:
    return response