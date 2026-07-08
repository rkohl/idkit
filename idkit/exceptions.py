class IdentifierError(Exception):
    """Base identifier exception."""


class IdentifierParseError(IdentifierError, ValueError):
    """Raised when an identifier cannot be parsed."""


class IdentifierValidationError(IdentifierError, ValueError):
    """Raised when an identifier fails validation."""
