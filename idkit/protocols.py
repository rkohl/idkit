from __future__ import annotations

from enum import StrEnum
from typing import Any, Protocol, Self


class SupportsIdentifier[G: StrEnum, S: StrEnum, R: StrEnum](Protocol):
    """Structural interface implemented by identifier-like values.

    Use this protocol when a function only needs the public identifier API and
    should accept either ``Identifier`` instances or compatible implementations.
    """

    @property
    def group(self) -> G: ...

    @property
    def source(self) -> S | None: ...

    @property
    def component(self) -> S | None: ...

    @property
    def role(self) -> R | None: ...

    @property
    def parts(self) -> tuple[G, S | None, S | None, R | None]: ...

    @property
    def string_parts(self) -> tuple[str, ...]: ...

    @property
    def namespace(self) -> str: ...

    @property
    def qualified(self) -> str: ...

    @property
    def value(self) -> str: ...

    @property
    def path(self) -> str: ...

    @property
    def slug(self) -> str: ...

    @property
    def metric_key(self) -> str: ...

    @property
    def cache_key(self) -> str: ...

    @property
    def event_topic(self) -> str: ...

    @property
    def has_source(self) -> bool: ...

    @property
    def has_component(self) -> bool: ...

    @property
    def has_role(self) -> bool: ...

    @property
    def has_action(self) -> bool: ...

    @property
    def is_complete(self) -> bool: ...

    def require_source(self) -> Self: ...

    def require_role(self) -> Self: ...

    def require_action(self) -> Self: ...

    def require_complete(self) -> Self: ...

    def to_dict(self) -> dict[str, Any]: ...


class Identifiable[G: StrEnum, S: StrEnum, R: StrEnum](Protocol):
    """Structural interface for objects that expose an ``identifier`` property."""

    @property
    def identifier(self) -> SupportsIdentifier[G, S, R]: ...
