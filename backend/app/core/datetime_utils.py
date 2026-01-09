from __future__ import annotations

from datetime import datetime, timezone


def utc_now() -> datetime:
    """
    Get current UTC datetime.
    
    This function provides a centralized way to get the current UTC time,
    making it easier to change timezone handling in the future if needed.
    
    Returns:
        Current UTC datetime with timezone awareness
    """
    return datetime.now(timezone.utc)


def to_utc(dt: datetime) -> datetime:
    """
    Convert a datetime to UTC if it's timezone-aware.
    
    Args:
        dt: Datetime to convert
        
    Returns:
        Datetime in UTC
    """
    if dt.tzinfo is None:
        # Naive datetime, assume it's already UTC
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
