from __future__ import annotations

from .namespaces import Namespace
from typing import Any, Protocol, Self
import uuid


class IdentityLike[GN: Namespace, SN: Namespace, RN: Namespace](Protocol):
    """
    Structural protocol for identifier-like objects.

    `Identities` describes the public interface required for an object
    to behave like an identifier, without requiring it to inherit from the
    concrete `Identifier` class.

    Use this protocol when a function, service, registry, logger, event bus,
    or configuration system only needs to read or validate an identifier.

    This allows different identifier implementations to be used interchangeably
    as long as they expose the same public API.

    Purpose:
        - Accept any object that behaves like an identifier.
        - Avoid coupling APIs to the concrete `Identifier` implementation.
        - Enable flexible testing, mocking, wrapping, or alternate identifier
          implementations.
        - Preserve type safety across custom enum sets.

    Format:
        Group::Source[:Component][-Role][<Unique>]

    Examples:
        system::runtime:agent-analyzer
        service::data:resource-ingester
        manage::workflow:pipeline-runner

    Use cases:
        - Service registries
        - Dependency injection containers
        - Event topic routing
        - Logging and metrics keys
        - Cache keys
        - Configuration lookup
        - Permission or policy matching
        - Testing with lightweight mock identifiers

    Example:
        def register(identifier: Identities[Group, Source, Role]) -> None:
            identifier.require_complete()
            registry[identifier.value] = identifier
    """

    @property
    def group(self) -> GN: ...

    @property
    def source(self) -> SN | None: ...

    @property
    def component(self) -> SN | None: ...

    @property
    def role(self) -> RN | None: ...

    @property
    def unique_id(self) -> str | None: ...

    @property
    def parts(self) -> tuple[GN, SN | None, SN | None, RN | None, str | None]: ...

    @property
    def string_parts(self) -> tuple[str, ...]: ...

    @property
    def segment(self) -> GN | SN | RN: ...

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

    @property
    def has_unique_id(self) -> bool: ...

    def require_source(self) -> Self: ...

    def require_role(self) -> Self: ...

    def require_action(self) -> Self: ...

    def require_complete(self) -> Self: ...

    def unique(self, unique_id: str | float | uuid.UUID) -> Self: ...

    def to_dict(self) -> dict[str, Any]: ...


class Identifiable[GN: Namespace, SN: Namespace, RN: Namespace](Protocol):
    """
    Structural protocol for objects that expose an identifier.

    `Identifiable` describes any object that can be identified by a stable,
    structured identifier through an `identifier` property.

    Use this protocol when you want to operate on application objects directly
    instead of passing identifiers around separately.

    An identifiable object may be a service, manager, controller, task,
    workflow, pipeline, repository, handler, plugin, module, or any other
    framework object that has a stable architectural identity.

    Purpose:
        - Establish a consistent identity contract across framework objects.
        - Allow registries, containers, event systems, and loggers to work with
          objects directly.
        - Keep identity attached to the object it represents.
        - Avoid duplicating identifier arguments throughout APIs.
        - Enable generic discovery and registration patterns.

    Example:
        class RuntimeAnalyzer:
            @property
            def identifier(self) -> AppIdentifier:
                return ID.system.runtime.agent.analyzer

        def register(item: Identifiable[Group, Source, Role]) -> None:
            registry[item.identifier] = item

    Common use cases:
        - Registering services by identity.
        - Routing events to identifiable handlers.
        - Creating logger names from object identity.
        - Mapping metrics to identifiable components.
        - Resolving dependencies from a container.
        - Discovering plugins, jobs, workflows, or tasks.
        - Grouping framework objects by namespace or parent identity.

    Design note:
        `Identifiable` should usually expose a stable, immutable identifier.
        For framework classes, the identifier is often best defined as a class
        attribute or read-only property because it represents what the object is,
        not mutable runtime state.
    """

    @property
    def identifier(self) -> IdentityLike[GN, SN, RN]: ...
