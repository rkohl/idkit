from __future__ import annotations

from .identity import Identity, IdentityNamespace
from .protocols import (
    Identifiable as IDKitIdentifiable,
    IdentityLike as IDKitIdentityLike,
)
from .namespaces import (
    GroupNamespace,
    OperationNamespace,
    RoleNamespace,
    SourceNamespace,
)


type Identifier = Identity[GroupNamespace, SourceNamespace, RoleNamespace]

type OperationIdentifier = Identity[GroupNamespace, SourceNamespace, OperationNamespace]

type IDLike = IDKitIdentityLike[GroupNamespace, SourceNamespace, RoleNamespace]

type IDable = IDKitIdentifiable[GroupNamespace, SourceNamespace, RoleNamespace]


"""
ID namespace

`ID` is the canonical entry point for creating 
identities throughout the application. All identities 
should originate from this shared instance rather
than being instantiated directly.

Examples:
    ID.system.runtime.agent.analyzer
    ID.service.data.resource.ingester
    ID.manage.workflow.pipeline.runner

The resulting identities are immutable, hashable, comparable, 
and can be used as dictionary keys, registry identifiers, 
event topics, metric names, cache keys, and logging 
namespaces.
"""
ID: Identifier = IdentityNamespace(
    group=GroupNamespace,
    source=SourceNamespace,
    role=RoleNamespace,
)


__all__ = [
    "ID",
    "Identifier",
    "OperationIdentifier",
    "IDLike",
    "IDable",
    "GroupNamespace",
    "SourceNamespace",
    "RoleNamespace",
    "OperationNamespace",
]
