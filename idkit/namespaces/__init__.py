from .group import GroupNamespace
from .source import SourceNamespace
from .role import RoleNamespace
from .operation import OperationNamespace
from typing import Protocol


class Namespace(Protocol):
    """
    The Namespace is a declarative value that provides a scope for the Identifier by organizing into logical segments.

    If subclasses `StrEnum` to provide a typed safe approach.

    Group — Where does it belong?
    Source — What is it?
    Component — Which part of it?
    Action — What does it do?
    """

    value: str


__all__ = [
    "GroupNamespace",
    "SourceNamespace",
    "RoleNamespace",
    "OperationNamespace",
    "Namespace",
]
