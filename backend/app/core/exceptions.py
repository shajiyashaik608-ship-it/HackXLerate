from typing import Optional, Any
from fastapi import Request, FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class AppException(Exception):
    """Base application domain exception."""
    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Any] = None
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details


class EntityNotFoundException(AppException):
    def __init__(self, entity_name: str, identifier: Any):
        super().__init__(
            message=f"{entity_name} with identifier '{identifier}' not found.",
            code="ENTITY_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )


class NotFoundException(AppException):
    def __init__(self, message: str = "Requested resource not found."):
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )


class AuthenticationException(AppException):
    def __init__(self, message: str = "Invalid authentication credentials."):
        super().__init__(
            message=message,
            code="AUTHENTICATION_FAILED",
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class UnauthorizedException(AuthenticationException):
    pass


class AuthorizationException(AppException):
    def __init__(self, message: str = "You do not have permission to access this resource."):
        super().__init__(
            message=message,
            code="FORBIDDEN",
            status_code=status.HTTP_403_FORBIDDEN
        )


class ForbiddenException(AuthorizationException):
    pass


class ValidationException(AppException):
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class MedicalExtractionException(AppException):
    def __init__(self, message: str = "Medical report extraction encountered an issue."):
        super().__init__(
            message=message,
            code="DOCUMENT_PROCESSING_FAILED",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class EmergencySymptomDetectedException(AppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="EMERGENCY_SYMPTOM_FLAGGED",
            status_code=status.HTTP_200_OK
        )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "req-unknown")
    payload = {
        "error": {
            "code": exc.code,
            "message": exc.message,
            "request_id": request_id
        }
    }
    if exc.details:
        payload["error"]["details"] = exc.details
    return JSONResponse(status_code=exc.status_code, content=payload)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "req-unknown")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "REQUEST_VALIDATION_ERROR",
                "message": "Invalid request parameters or payload.",
                "request_id": request_id,
                "details": exc.errors()
            }
        }
    )


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
