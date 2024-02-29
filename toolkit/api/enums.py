"""Enumeration types for API-related constants."""

from enum import Enum


class AuthScheme(Enum):
    """Enumeration for various authentication schemes."""

    BASIC = "Basic"
    BEARER = "Bearer"
    DIGEST = "Digest"
