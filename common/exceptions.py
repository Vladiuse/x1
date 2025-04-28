class AppException(Exception):
    """Base application exception"""


class CantGetPageContent(AppException):
    """Cant get page content"""