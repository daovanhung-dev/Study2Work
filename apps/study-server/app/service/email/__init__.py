"""External email-provider boundaries for the Study service."""

from app.service.email.provider import (
    StubVerificationEmailProvider,
    VerificationDispatchResult,
    VerificationEmailProvider,
    VerificationEmailProviderError,
    get_verification_email_provider,
)

__all__ = [
    "StubVerificationEmailProvider",
    "VerificationDispatchResult",
    "VerificationEmailProvider",
    "VerificationEmailProviderError",
    "get_verification_email_provider",
]
