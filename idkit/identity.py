from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Iterator, Self

from .namespaces.namespace import Namespace


@dataclass(frozen=True)
class Identity[GN: Namespace, SN: Namespace, RN: Namespace]:
    """
    Represents the immutable identity of an architectural component.

    An `Identity` provides a strongly typed, structured representation of an
    object's identity using the following format:

        Group::Source[:Component][-Role][<Unique>]

    Unlike ordinary strings, an `Identity` preserves the semantic meaning of
    each segment while providing utilities for parsing, validation,
    serialization, comparison, hierarchy traversal, and namespace matching.

    Identities are immutable, hashable, comparable, and suitable for use as
    dictionary keys, registry identifiers, event topics, metric names, cache
    keys, and logging namespaces.

    Format:
        Group::Source[:Component][-Role][<Unique>]

    Components:
        Group
            The architectural domain or category to which the identity belongs.

        Source
            The primary object, resource, or subsystem represented by the
            identity.

        Component
            An optional specialization of the source representing a specific
            implementation or subcomponent.

        Role
            An optional stable responsibility or architectural role associated
            with the identity.

    Examples:
        system::runtime
        system::runtime:agent
        system::runtime:agent-analyzer

        service::data:resource-ingester

        manage::workflow:pipeline-runner

    Construction:
        Identities are normally created through an `IdentityNamespace`
        using fluent dot notation.

        Example:
            identity = ID.system.runtime.agent.analyzer

    Features:
        - Immutable and hashable.
        - Strongly typed through namespace enums.
        - Supports fluent construction.
        - String serialization and parsing.
        - Hierarchical parent traversal.
        - Prefix namespace matching.
        - Dictionary and JSON serialization.
        - Suitable for registry, dependency injection, logging, metrics,
          configuration, routing, and discovery systems.

    Design Notes:
        An `Identity` describes what an object *is*, not what it is currently
        doing.

        Runtime behavior should be represented separately using an
        `IdentifierOperation`.

        Example:
            identity = ID.service.data.resource.ingester
            operation = IdentifierOperation.ingest

    See Also:
        IdentityNamespace
            Entry point used to construct identities.

        IdentityLike
            Structural protocol implemented by identity-like objects.

        Identifiable
            Structural protocol for objects exposing an `identity` property.
    """

    group: GN
    source: SN | None = None
    component: SN | None = None
    role: RN | None = None
    unique_id: str | None = None

    source_enum: type[SN] | None = field(default=None, repr=False, compare=False)
    role_enum: type[RN] | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.component is not None and self.source is None:
            raise IdentifierValidationError(
                "Identifier cannot have a component without a source."
            )

        if self.unique_id is not None:
            if self.role is None:
                raise IdentifierValidationError(
                    "Identifier cannot have a unique id without a role."
                )

            if not self.unique_id:
                raise IdentifierValidationError("Identifier unique id cannot be empty.")

    def __getattr__(self, name: str) -> Identity[GN, SN, RN]:
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

    @property
    def has_unique_id(self) -> bool:
        return self.unique_id is not None

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

    def with_source(self, source: SN) -> Self:
        if self.source is not None:
            raise IdentifierValidationError("Identifier already has a source.")

        return type(self)(
            group=self.group,
            source=source,
            component=self.component,
            role=self.role,
            unique_id=self.unique_id,
            source_enum=self.source_enum,
            role_enum=self.role_enum,
        )

    def with_component(self, component: SN) -> Self:
        if self.source is None:
            raise IdentifierValidationError("Cannot set component before source.")

        if self.component is not None:
            raise IdentifierValidationError("Identifier already has a component.")

        return type(self)(
            group=self.group,
            source=self.source,
            component=component,
            role=self.role,
            unique_id=self.unique_id,
            source_enum=self.source_enum,
            role_enum=self.role_enum,
        )

    def with_role(self, role: RN) -> Self:
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

    def unique(self, unique_id: str) -> Self:
        if self.role is None:
            raise IdentifierValidationError("Cannot set unique id before role.")

        if self.unique_id is not None:
            raise IdentifierValidationError("Identifier already has a unique id.")

        return type(self)(
            group=self.group,
            source=self.source,
            component=self.component,
            role=self.role,
            unique_id=unique_id,
            source_enum=self.source_enum,
            role_enum=self.role_enum,
        )

    def with_source_or_component(self, source: SN) -> Self:
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
            unique_id=None,
            source_enum=self.source_enum,
            role_enum=self.role_enum,
        )

    def without_component(self) -> Self:
        return type(self)(
            group=self.group,
            source=self.source,
            component=None,
            role=self.role,
            unique_id=self.unique_id,
            source_enum=self.source_enum,
            role_enum=self.role_enum,
        )

    def without_source(self) -> Self:
        return type(self)(
            group=self.group,
            source=None,
            component=None,
            role=self.role,
            unique_id=self.unique_id,
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

    def matches(self, other: Identity[GN, SN, RN] | str) -> bool:
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

        if other.unique_id is not None and self.unique_id != other.unique_id:
            return False

        return True

    @property
    def parts(self) -> tuple[GN, SN | None, SN | None, RN | None, str | None]:
        return self.group, self.source, self.component, self.role, self.unique_id

    @property
    def string_parts(self) -> tuple[str, ...]:
        return tuple(
            part.value
            for part in (self.group, self.source, self.component, self.role)
            if part is not None
        )

    @property
    def segment(self) -> GN | SN | RN:
        for part in (self.role, self.component, self.source, self.group):
            if part is not None:
                return part

        raise IdentifierValidationError("Identifier requires at least a group.")

    @property
    def namespace(self) -> str:
        if self.source is None:
            return self.group.value

        value = f"{self.group.value}::{self.source.value}"

        if self.component is not None:
            value += f":{self.component.value}"

        return value

    @property
    def qualified(self) -> str:
        value = self.namespace

        if self.role is not None:
            value = f"{value}-{self.role.value}"

        if self.unique_id is not None:
            value = f"{value}<{self.unique_id}>"

        return value

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
            "unique_id": self.unique_id,
            "segment": self.segment.value,
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
        if isinstance(other, Identity):
            return self.parts == other.parts

        if isinstance(other, str):
            return self.value == other

        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Identity):
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
        group_enum: type[GN],
        source_enum: type[SN],
        role_enum: type[RN],
    ) -> Identity[GN, SN, RN]:
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
                    f"Invalid identifier '{value}'. Expected format: Group::Source[:Component][-Role][<Unique>]."
                ) from exc

        try:
            group_part, rest = value.split("::", 1)
        except ValueError as exc:
            raise IdentifierParseError(
                f"Invalid identifier '{value}'. Expected format: Group::Source[:Component][-Role][<Unique>]."
            ) from exc

        if not group_part:
            raise IdentifierParseError("Group cannot be empty.")

        try:
            parsed_group = group_enum(group_part)
        except ValueError as exc:
            raise IdentifierParseError(f"Invalid group '{group_part}'.") from exc

        if not rest:
            raise IdentifierParseError("Source cannot be empty.")

        parsed_unique_id: str | None = None

        if "<" in rest or ">" in rest:
            if rest.count("<") != 1 or rest.count(">") != 1 or not rest.endswith(">"):
                raise IdentifierParseError(
                    f"Invalid identifier '{value}'. Expected format: Group::Source[:Component][-Role][<Unique>]."
                )

            rest, unique_part = rest[:-1].split("<", 1)

            if not unique_part:
                raise IdentifierParseError("Unique id cannot be empty.")

            parsed_unique_id = unique_part

        parsed_role: RN | None = None

        if "-" in rest:
            rest, role_part = rest.split("-", 1)

            if not role_part:
                raise IdentifierParseError("role cannot be empty.")

            try:
                parsed_role = role_enum(role_part)
            except ValueError as exc:
                raise IdentifierParseError(f"Invalid role '{role_part}'.") from exc

        if not rest:
            raise IdentifierParseError("Source cannot be empty.")

        parsed_component: SN | None = None

        if ":" in rest:
            source_part, component_part = rest.split(":", 1)

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
            unique_id=parsed_unique_id,
            source_enum=source_enum,
            role_enum=role_enum,
        )


class IdentityNamespace[GN: Namespace, SN: Namespace, RN: Namespace]:
    """
    Entry point for constructing strongly typed identities.

    `IdentityNamespace` provides the fluent, dot-notation interface used to build
    immutable `Identity` instances from the configured group, source, and role
    enumerations.

    Rather than constructing identities manually, applications should create a
    single root instance and use it as the canonical factory throughout the
    project.

    Format:
        Group::Source[:Component][-Role][<Unique>]

    Example:
        ID.system.runtime.agent.analyzer
        # system::runtime:agent-analyzer

        ID.service.data.resource.ingester
        # service::data:resource-ingester

        ID.manage.workflow.pipeline.runner
        # manage::workflow:pipeline-runner

    Purpose:
        - Serves as the namespace for all identities.
        - Enforces the configured enum types for groups, sources, and roles.
        - Provides a fluent, discoverable API through dot notation.
        - Eliminates manual string construction.
        - Creates immutable, strongly typed `Identity` objects.
        - Provides parsing of serialized identities back into objects.

    Use cases:
        - Creating identities for framework components.
        - Registering services and plugins.
        - Dependency injection.
        - Event routing.
        - Logging and metrics.
        - Configuration lookup.
        - Cache keys.
        - Service discovery.

    Design:
        A project will typically expose a single shared instance:

            ID = IdentityRoot(
                group_enum=IdentifierGroup,
                source_enum=IdentifierSource,
                role_enum=IdentifierRole,
            )

        This instance acts as the root of the project's identity hierarchy and
        should be reused throughout the application.
    """

    def __init__(
        self,
        *,
        group: type[GN],
        source: type[SN],
        role: type[RN],
    ):
        self.group = group
        self.source = source
        self.role = role

    def __getattr__(self, name: str) -> Identity[GN, SN, RN]:
        if name in self.group.__members__:
            return Identity(
                group=self.group[name],
                source_enum=self.source,
                role_enum=self.role,
            )

        raise AttributeError(name)

    def parse(self, value: str) -> Identity[GN, SN, RN]:
        return Identity.parse(
            value,
            group_enum=self.group,
            source_enum=self.source,
            role_enum=self.role,
        )


class IdentifierError(Exception):
    """Base identifier exception."""


class IdentifierParseError(IdentifierError, ValueError):
    """Raised when an identifier cannot be parsed."""


class IdentifierValidationError(IdentifierError, ValueError):
    """Raised when an identifier fails validation."""
