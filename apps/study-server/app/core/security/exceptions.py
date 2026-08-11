"""Security-related exceptions."""


class TokenError(Exception):
    """Raised when a token is invalid, expired, or misconfigured."""
