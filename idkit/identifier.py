from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Iterator, Self

from .exceptions import IdentifierParseError, IdentifierValidationError


@dataclass(frozen=True)
class Identifier[G: StrEnum, S: StrEnum, R: StrEnum]:
    """
    Immutable typed identifier value.

    The identifier format is:

        Group::Source[-Component][+role]

    The same source enum is used for both the required ``Source`` segment and
    the optional ``Component`` segment. Instances support fluent construction
    through attribute access when created from an ``IdentifierRoot``.

    Examples:
        system::runtime
        system::runtime-agent
        system::runtime-agent+analyzer
    """

    group: G
    source: S | None = None
    component: S | None = None
    role: R | None = None

    source_enum: type[S] | None = field(default=None, repr=False, compare=False)
    role_enum: type[R] | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.component is not None and self.source is None:
            raise IdentifierValidationError(
                "Identifier cannot have a component without a source."
            )

    def __getattr__(self, name: str) -> Identifier[G, S, R]:
        if self.source_enum and name in self.source_enum.__members__:
            if self.source is None or self.component is None:
                return self.with_source_or_component(self.source_enum[name])

        if self.role_enum and name in self.role_enum.__members__:
            return self.with_role(self.role_enum[name])

        raise AttributeError(name)

    @property
    def has_source(self) -> bool:
        return self.source is not None

    @property
    def has_component(self) -> bool:
        return self.component is not None

    @property
    def has_role(self) -> bool:
        return self.role is not None

    @property
    def has_action(self) -> bool:
        return self.has_role

    @property
    def is_complete(self) -> bool:
        return self.source is not None and self.role is not None

    def require_source(self) -> Self:
        if self.source is None:
            raise IdentifierValidationError("Identifier requires a source.")
        return self

    def require_role(self) -> Self:
        if self.role is None:
            raise IdentifierValidationError("Identifier requires an role.")
        return self

    def require_action(self) -> Self:
        return self.require_role()

    def require_complete(self) -> Self:
        self.require_source()
        self.require_role()
        return self

    def with_source(self, source: S) -> Self:
        if self.source is not None:
            raise IdentifierValidationError("Identifier already has a source.")

        return type(self)(
            group=self.group,
            source=source,
            component=self.component,
            role=self.role,
            source_enum=self.source_enum,
            role_enum=self.role_enum,
        )

    def with_component(self, component: S) -> Self:
        if self.source is None:
            raise IdentifierValidationError("Cannot set component before source.")

        if self.component is not None:
            raise IdentifierValidationError("Identifier already has a component.")

        return type(self)(
            group=self.group,
            source=self.source,
            component=component,
            role=self.role,
            source_enum=self.source_enum,
            role_enum=self.role_enum,
        )

    def with_role(self, role: R) -> Self:
        if self.role is not None:
            raise IdentifierValidationError("Identifier already has an role.")

        return type(self)(
            group=self.group,
            source=self.source,
            component=self.component,
            role=role,
            source_enum=self.source_enum,
            role_enum=self.role_enum,
        )

    def with_source_or_component(self, source: S) -> Self:
        if self.source is None:
            return self.with_source(source)

        if self.component is None:
            return self.with_component(source)

        raise IdentifierValidationError(
            "Identifier already has both source and component."
        )

    def without_role(self) -> Self:
        return type(self)(
            group=self.group,
            source=self.source,
            component=self.component,
            role=None,
            source_enum=self.source_enum,
            role_enum=self.role_enum,
        )

    def without_component(self) -> Self:
        return type(self)(
            group=self.group,
            source=self.source,
            component=None,
            role=self.role,
            source_enum=self.source_enum,
            role_enum=self.role_enum,
        )

    def without_source(self) -> Self:
        return type(self)(
            group=self.group,
            source=None,
            component=None,
            role=self.role,
            source_enum=self.source_enum,
            role_enum=self.role_enum,
        )

    @property
    def parent(self) -> Self:
        if self.role is not None:
            return self.without_role()

        if self.component is not None:
            return self.without_component()

        if self.source is not None:
            return type(self)(
                group=self.group,
                source_enum=self.source_enum,
                role_enum=self.role_enum,
            )

        return self

    @property
    def parents(self) -> tuple[Self, ...]:
        items: list[Self] = []
        current = self

        while current.parent != current:
            current = current.parent
            items.append(current)

        return tuple(items)

    def matches(self, other: Identifier[G, S, R] | str) -> bool:
        """
        Prefix-style hierarchy match.

        ID.system.runtime.agent.analyzer.matches(ID.system.runtime) == True
        """
        if isinstance(other, str):
            if self.source_enum is None or self.role_enum is None:
                return self.value == other

            try:
                other = type(self).parse(
                    other,
                    group_enum=type(self.group),
                    source_enum=self.source_enum,
                    role_enum=self.role_enum,
                )
            except IdentifierParseError:
                return False

        if self.group != other.group:
            return False

        if other.source is not None and self.source != other.source:
            return False

        if other.component is not None and self.component != other.component:
            return False

        if other.role is not None and self.role != other.role:
            return False

        return True

    @property
    def parts(self) -> tuple[G, S | None, S | None, R | None]:
        return self.group, self.source, self.component, self.role

    @property
    def string_parts(self) -> tuple[str, ...]:
        return tuple(
            part.value
            for part in (self.group, self.source, self.component, self.role)
            if part is not None
        )

    @property
    def namespace(self) -> str:
        if self.source is None:
            return self.group.value

        value = f"{self.group.value}::{self.source.value}"

        if self.component is not None:
            value += f"-{self.component.value}"

        return value

    @property
    def qualified(self) -> str:
        if self.role is None:
            return self.namespace

        return f"{self.namespace}+{self.role.value}"

    @property
    def value(self) -> str:
        return self.qualified

    @property
    def path(self) -> str:
        return "/".join(self.string_parts)

    @property
    def slug(self) -> str:
        return "-".join(self.string_parts)

    @property
    def metric_key(self) -> str:
        return ".".join(self.string_parts)

    @property
    def cache_key(self) -> str:
        return self.value

    @property
    def event_topic(self) -> str:
        return self.path

    def to_dict(self) -> dict[str, Any]:
        return {
            "group": self.group.value,
            "source": self.source.value if self.source else None,
            "component": self.component.value if self.component else None,
            "role": self.role.value if self.role else None,
            "namespace": self.namespace,
            "qualified": self.qualified,
            "path": self.path,
            "slug": self.slug,
            "metric_key": self.metric_key,
            "cache_key": self.cache_key,
            "event_topic": self.event_topic,
            "value": self.value,
        }

    def __iter__(self) -> Iterator[StrEnum]:
        yield self.group

        if self.source is not None:
            yield self.source

        if self.component is not None:
            yield self.component

        if self.role is not None:
            yield self.role

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"Identifier('{self.value}')"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Identifier):
            return self.parts == other.parts

        if isinstance(other, str):
            return self.value == other

        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Identifier):
            return self.value < other.value

        if isinstance(other, str):
            return self.value < other

        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.parts)

    @classmethod
    def parse(
        cls,
        value: str,
        *,
        group_enum: type[G],
        source_enum: type[S],
        role_enum: type[R],
    ) -> Identifier[G, S, R]:
        if not value:
            raise IdentifierParseError("Identifier cannot be empty.")

        if "::" not in value:
            try:
                return cls(
                    group=group_enum(value),
                    source_enum=source_enum,
                    role_enum=role_enum,
                )
            except ValueError as exc:
                raise IdentifierParseError(
                    f"Invalid identifier '{value}'. Expected format: Group::Source[-Component][+role]."
                ) from exc

        try:
            group_part, rest = value.split("::", 1)
        except ValueError as exc:
            raise IdentifierParseError(
                f"Invalid identifier '{value}'. Expected format: Group::Source[-Component][+role]."
            ) from exc

        if not group_part:
            raise IdentifierParseError("Group cannot be empty.")

        try:
            parsed_group = group_enum(group_part)
        except ValueError as exc:
            raise IdentifierParseError(f"Invalid group '{group_part}'.") from exc

        if not rest:
            raise IdentifierParseError("Source cannot be empty.")

        parsed_role: R | None = None

        if "+" in rest:
            rest, role_part = rest.split("+", 1)

            if not role_part:
                raise IdentifierParseError("role cannot be empty.")

            try:
                parsed_role = role_enum(role_part)
            except ValueError as exc:
                raise IdentifierParseError(f"Invalid role '{role_part}'.") from exc

        if not rest:
            raise IdentifierParseError("Source cannot be empty.")

        parsed_component: S | None = None

        if "-" in rest:
            source_part, component_part = rest.split("-", 1)

            if not source_part:
                raise IdentifierParseError("Source cannot be empty.")

            if not component_part:
                raise IdentifierParseError("Component cannot be empty.")

            try:
                parsed_source = source_enum(source_part)
            except ValueError as exc:
                raise IdentifierParseError(f"Invalid source '{source_part}'.") from exc

            try:
                parsed_component = source_enum(component_part)
            except ValueError as exc:
                raise IdentifierParseError(
                    f"Invalid component '{component_part}'."
                ) from exc

        else:
            try:
                parsed_source = source_enum(rest)
            except ValueError as exc:
                raise IdentifierParseError(f"Invalid source '{rest}'.") from exc

        return cls(
            group=parsed_group,
            source=parsed_source,
            component=parsed_component,
            role=parsed_role,
            source_enum=source_enum,
            role_enum=role_enum,
        )
