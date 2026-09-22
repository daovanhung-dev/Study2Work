from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class VerificationDispatchResult:
    """Provider result used by the public verification-dispatch response."""

    status: str
    reason: str | None = None


class VerificationEmailProviderError(RuntimeError):
    """Raised when a provider cannot accept a verification dispatch."""


class VerificationEmailProvider(Protocol):
    """Boundary for a provider that accepts verification-email dispatches."""

    def dispatch(
        self,
        *,
        user_id: int,
        email: str,
        trace_id: str,
    ) -> VerificationDispatchResult:
        """Accept a verification dispatch or raise a provider error."""


class StubVerificationEmailProvider:
    """Development provider that accepts without sending a real email."""

    def dispatch(
        self,
        *,
        user_id: int,
        email: str,
        trace_id: str,
    ) -> VerificationDispatchResult:
        del user_id, email, trace_id
        return VerificationDispatchResult(status="accepted")


def get_verification_email_provider() -> VerificationEmailProvider:
    """Return the default provider used by the current Study runtime."""

    return StubVerificationEmailProvider()
