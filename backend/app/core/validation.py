from __future__ import annotations

from typing import Any

from fastapi import HTTPException

from .constants import (
    COMMENT_MAX_LENGTH,
    COMMENT_MIN_LENGTH,
    TABLE_NAME_MAX_LENGTH,
    TABLE_NAME_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
    VALID_PAYMENT_TYPES,
    VALID_ROLES,
    VALID_SESSION_STATUSES,
)


class ValidationError(Exception):
    """Exception raised for validation errors."""
    pass


def validate_table_name(name: str) -> str:
    """
    Validate table name.
    
    Args:
        name: Table name to validate
        
    Returns:
        Validated table name
        
    Raises:
        ValidationError: If validation fails
    """
    if not name:
        raise ValidationError("Table name is required")
    
    name = name.strip()
    
    if len(name) < TABLE_NAME_MIN_LENGTH:
        raise ValidationError(f"Table name must be at least {TABLE_NAME_MIN_LENGTH} character(s)")
    
    if len(name) > TABLE_NAME_MAX_LENGTH:
        raise ValidationError(f"Table name must not exceed {TABLE_NAME_MAX_LENGTH} characters")
    
    # Allow alphanumeric, spaces, and common punctuation
    if not any(c.isalnum() for c in name):
        raise ValidationError("Table name must contain at least one alphanumeric character")
    
    return name


def validate_username(username: str) -> str:
    """
    Validate username.
    
    Args:
        username: Username to validate
        
    Returns:
        Validated username
        
    Raises:
        ValidationError: If validation fails
    """
    if not username:
        raise ValidationError("Username is required")
    
    username = username.strip()
    
    if len(username) < USERNAME_MIN_LENGTH:
        raise ValidationError(f"Username must be at least {USERNAME_MIN_LENGTH} character(s)")
    
    if len(username) > USERNAME_MAX_LENGTH:
        raise ValidationError(f"Username must not exceed {USERNAME_MAX_LENGTH} characters")
    
    # Allow alphanumeric, underscore, hyphen, and dot
    if not all(c.isalnum() or c in "_.-" for c in username):
        raise ValidationError("Username can only contain alphanumeric characters, underscores, hyphens, and dots")
    
    return username


def validate_role(role: str) -> str:
    """
    Validate user role.
    
    Args:
        role: Role to validate
        
    Returns:
        Validated role
        
    Raises:
        ValidationError: If validation fails
    """
    if role not in VALID_ROLES:
        raise ValidationError(f"Invalid role. Must be one of: {', '.join(VALID_ROLES)}")
    return role


def validate_session_status(status: str) -> str:
    """
    Validate session status.
    
    Args:
        status: Status to validate
        
    Returns:
        Validated status
        
    Raises:
        ValidationError: If validation fails
    """
    if status not in VALID_SESSION_STATUSES:
        raise ValidationError(f"Invalid status. Must be one of: {', '.join(VALID_SESSION_STATUSES)}")
    return status


def validate_payment_type(payment_type: str) -> str:
    """
    Validate payment type.
    
    Args:
        payment_type: Payment type to validate
        
    Returns:
        Validated payment type
        
    Raises:
        ValidationError: If validation fails
    """
    if payment_type not in VALID_PAYMENT_TYPES:
        raise ValidationError(f"Invalid payment type. Must be one of: {', '.join(VALID_PAYMENT_TYPES)}")
    return payment_type


def validate_comment(comment: str) -> str:
    """
    Validate comment.
    
    Args:
        comment: Comment to validate
        
    Returns:
        Validated comment
        
    Raises:
        ValidationError: If validation fails
    """
    if not comment:
        raise ValidationError("Comment is required")
    
    comment = comment.strip()
    
    if len(comment) < COMMENT_MIN_LENGTH:
        raise ValidationError(f"Comment must be at least {COMMENT_MIN_LENGTH} character(s)")
    
    if len(comment) > COMMENT_MAX_LENGTH:
        raise ValidationError(f"Comment must not exceed {COMMENT_MAX_LENGTH} characters")
    
    return comment


def validate_seats_count(seats_count: int | None, default: int = 24) -> int:
    """
    Validate seats count.
    
    Args:
        seats_count: Seats count to validate
        default: Default value if seats_count is None
        
    Returns:
        Validated seats count
        
    Raises:
        ValidationError: If validation fails
    """
    from .constants import DEFAULT_SEATS_COUNT, MAX_SEATS_COUNT, MIN_SEATS_COUNT
    
    if seats_count is None:
        seats_count = default
    
    if seats_count < MIN_SEATS_COUNT:
        raise ValidationError(f"Seats count must be at least {MIN_SEATS_COUNT}")
    
    if seats_count > MAX_SEATS_COUNT:
        raise ValidationError(f"Seats count must not exceed {MAX_SEATS_COUNT}")
    
    return seats_count


def validate_amount(amount: int, allow_zero: bool = False) -> int:
    """
    Validate amount (positive integer).
    
    Args:
        amount: Amount to validate
        allow_zero: Whether zero is allowed
        
    Returns:
        Validated amount
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(amount, int):
        raise ValidationError("Amount must be an integer")
    
    if allow_zero and amount == 0:
        return 0
    
    if amount <= 0:
        raise ValidationError("Amount must be positive")
    
    return amount


def to_http_exception(exc: ValidationError) -> HTTPException:
    """
    Convert a ValidationError to an HTTPException.
    
    Args:
        exc: Validation exception
        
    Returns:
        HTTPException with status code 400
    """
    return HTTPException(status_code=400, detail=str(exc))
