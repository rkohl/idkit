from __future__ import annotations

from enum import StrEnum

from .identifier import Identifier


class IdentifierRoot[G: StrEnum, S: StrEnum, R: StrEnum]:
    """Entry point for building and parsing typed identifiers.

    An ``IdentifierRoot`` binds the enum types that define the valid groups,
    sources/components, and actions for a package. Attribute access on the root
    starts a new identifier from a group name, for example ``ID.system``.
    """

    def __init__(
        self,
        *,
        group: type[G],
        source: type[S],
        role: type[R],
    ):
        self.group = group
        self.source = source
        self.role = role

    def __getattr__(self, name: str) -> Identifier[G, S, R]:
        if name in self.group.__members__:
            return Identifier(
                group=self.group[name],
                source_enum=self.source,
                role_enum=self.role,
            )

        raise AttributeError(name)

    def parse(self, value: str) -> Identifier[G, S, R]:
        return Identifier.parse(
            value,
            group_enum=self.group,
            source_enum=self.source,
            role_enum=self.role,
        )


IDRoot = IdentifierRoot
"""Short alias for `IdentifierRoot`"""
