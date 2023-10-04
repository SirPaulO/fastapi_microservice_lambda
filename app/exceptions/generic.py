from enum import Enum

from fastapi_exceptionshandler import APIError


class GenericException(APIError):
    """
    Generic Exception class for examples.
    Try to make your own exceptions with more meaningful messages and error codes.
    Note that the status code can be changed according to the error code
    """

    class ErrorCode(Enum):
        Generic_Exception = "Generic error"
        Incorrect_Sum = "Incorrect Sum"
        Not_Found = "Not found"

    def __init__(self, error_code: ErrorCode) -> None:
        super().__init__(error_code)
        if error_code == self.ErrorCode.Generic_Exception:
            self.status_code = 406
        elif error_code == self.ErrorCode.Not_Found:
            self.status_code = 404
