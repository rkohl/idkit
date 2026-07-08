from __future__ import annotations

from .identifier import Identifier
from .protocols import Identifiable, SupportsIdentifier
from .root import IdentifierRoot
from .enums import (
    IdentifierGroup,
    IdentifierOperation,
    IdentifierRole,
    IdentifierSource,
)


type IDKitIdentifier = Identifier[IdentifierGroup, IdentifierSource, IdentifierRole]

type IDKitOperationIdentifier = Identifier[
    IdentifierGroup, IdentifierSource, IdentifierOperation
]

type IDKitIdentifierRoot = IdentifierRoot[
    IdentifierGroup, IdentifierSource, IdentifierRole
]

type IDKitIdentifierLike = SupportsIdentifier[
    IdentifierGroup, IdentifierSource, IdentifierRole
]

type IDKitIdentifiable = Identifiable[IdentifierGroup, IdentifierSource, IdentifierRole]

type AppIdentifier = IDKitIdentifier
type AppIdentifierRoot = IDKitIdentifierRoot
type AppIdentifierLike = IDKitIdentifierLike
type AppIdentifiable = IDKitIdentifiable


ID: IDKitIdentifierRoot = IdentifierRoot(
    group=IdentifierGroup,
    source=IdentifierSource,
    role=IdentifierRole,
)


__all__ = [
    "ID",
    "AppIdentifier",
    "AppIdentifierRoot",
    "AppIdentifierLike",
    "AppIdentifiable",
    "IDKitIdentifier",
    "IDKitOperationIdentifier",
    "IDKitIdentifierRoot",
    "IDKitIdentifierLike",
    "IDKitIdentifiable",
    "IdentifierGroup",
    "IdentifierSource",
    "IdentifierRole",
    "IdentifierOperation",
]
