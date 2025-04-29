import requests
from requests.exceptions import RequestException


class RequestSender:

    def get_content(self, url: str, attempts:int = 2) -> str:
        if attempts <= 0:
            raise ValueError('attempts must be positive integer')
        last_error = None
        for _ in range(attempts):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.text
            except RequestException as error:
                last_error = error
        raise last_error
