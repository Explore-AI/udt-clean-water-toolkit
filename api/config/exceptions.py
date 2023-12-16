from fastapi import HTTPException, status


class MethodNotAllowed(HTTPException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED

    def __init__(self, status_code=None, detail=None, headers=None):
        status_code = status_code or self.status_code
        if detail is None:
            detail = "Method not allowed."
        super().__init__(self.status_code, detail, headers)


class ParseError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, status_code=None, detail=None, headers=None):
        status_code = status_code or self.status_code
        if detail is None:
            detail = "Failed to parse data."
        super().__init__(status_code, detail, headers)


class ValidationError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, status_code=None, detail=None, headers=None):
        status_code = status_code or self.status_code
        if detail is None:
            detail = "Failed to validated data"
        super().__init__(status_code, detail, headers)
