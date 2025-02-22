from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class ServiceError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)


def error_handler(exc: Exception):
    if isinstance(exc, ServiceError):
        return {"error": {"code": exc.code, "message": exc.message}}
    return {"error": {"code": 1000, "message": "An unexpected error occurred."}}


def service_error_response(exc: ServiceError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"error": {"code": exc.code, "message": exc.message}}),
    )
