class BaseException(Exception):
    message: str = "Internal Server Error"

    def __init__(self, msg: str | None = None) -> None:
        self.message = msg or self.message


class NotFoundException(BaseException):
    message: str = "Not Found"
