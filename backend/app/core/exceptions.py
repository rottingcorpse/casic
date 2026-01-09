from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status


class BaseAppException(Exception):
    """Base exception for all application-specific exceptions."""

    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(BaseAppException):
    """Exception raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class ForbiddenException(BaseAppException):
    """Exception raised when access is forbidden."""

    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class BadRequestException(BaseAppException):
    """Exception raised for bad requests."""

    def __init__(self, message: str = "Bad request"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class ConflictException(BaseAppException):
    """Exception raised when a conflict occurs (e.g., duplicate resource)."""

    def __init__(self, message: str = "Conflict"):
        super().__init__(message, status.HTTP_409_CONFLICT)


class UnauthorizedException(BaseAppException):
    """Exception raised when authentication is required."""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class ValidationException(BaseAppException):
    """Exception raised when validation fails."""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)


def to_http_exception(exc: BaseAppException) -> HTTPException:
    """
    Convert an application exception to an HTTPException.
    
    Args:
        exc: Application exception
        
    Returns:
        HTTPException with appropriate status code and detail
    """
    return HTTPException(status_code=exc.status_code, detail=exc.message)


class ErrorResponse:
    """Standard error response structure."""

    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert error response to dictionary."""
        result: dict[str, Any] = {"message": self.message}
        if self.error_code:
            result["error_code"] = self.error_code
        if self.details:
            result["details"] = self.details
        return result


# Common error messages
class ErrorMessages:
    """Commonly used error messages."""

    SESSION_NOT_FOUND = "Session not found"
    SEAT_NOT_FOUND = "Seat not found"
    TABLE_NOT_FOUND = "Table not found"
    USER_NOT_FOUND = "User not found"
    
    NO_TABLE_ASSIGNED = "No table assigned"
    TABLE_ID_REQUIRED = "table_id is required for superadmin"
    FORBIDDEN_FOR_TABLE = "Forbidden for this table"
    FORBIDDEN_FOR_SESSION = "Forbidden for this session"
    
    SESSION_ALREADY_OPEN = "Session already open for this table"
    DEALER_ALREADY_ASSIGNED = "Dealer is already assigned to another active session"
    DEALER_REQUIRED = "Dealer is required to start a session"
    INVALID_DEALER = "Invalid dealer selected"
    INVALID_WAITER = "Invalid waiter selected"
    
    DEALER_CANNOT_SPECIFY_TABLE = "Dealers cannot specify table_id"
    DEALER_MUST_BE_ASSIGNED = "Dealers must be assigned to a session"
    
    TABLE_ADMIN_REQUIRES_TABLE = "table_id is required for table_admin role"
    DEALER_SHOULD_NOT_HAVE_TABLE = "dealer role should not have table_id"
    
    USERNAME_REQUIRED = "Username is required"
    USERNAME_EXISTS = "Username already exists"
    TABLE_NAME_REQUIRED = "Table name is required"
    TABLE_NAME_EXISTS = "Table name already exists"
    
    INVALID_DATE_FORMAT = "Invalid date format (expected YYYY-MM-DD)"
    AMOUNT_CANNOT_BE_ZERO = "Amount cannot be zero"
    NO_CREDIT_FOUND = "No credit found for this player"
    AMOUNT_EXCEEDS_CREDIT = "Amount exceeds available credit"
    
    ONLY_CLOSE_CREDIT_FOR_CLOSED = "Can only close credit for closed sessions"
    NO_HISTORY = "No history"
