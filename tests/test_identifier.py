import pytest

import idkit
from idkit import (
    ID,
    GroupNamespace,
    IDLike,
    IDable,
    Identifiable,
    Identifier,
    IdentifierError,
    IdentifierParseError,
    IdentifierValidationError,
    Identity,
    IdentityLike,
    IdentityNamespace,
    OperationIdentifier,
    OperationNamespace,
    RoleNamespace,
    SourceNamespace,
)


def test_identifier_value():
    identifier = ID.system.runtime.agent.analyzer
    assert str(identifier) == "system::runtime:agent-analyzer"
    assert identifier.value == "system::runtime:agent-analyzer"


def test_unique_identifier_value():
    identifier = ID.workflow.manager.data.adapter.unique("Index")

    assert str(identifier) == "workflow::manager:data-adapter<Index>"
    assert identifier.value == "workflow::manager:data-adapter<Index>"
    assert identifier.unique_id == "Index"
    assert identifier.has_unique_id is True


def test_namespace():
    identifier = ID.system.runtime.agent.analyzer
    assert identifier.namespace == "system::runtime:agent"


def test_parse():
    identifier = ID.system.runtime.agent.analyzer
    parsed = ID.parse("system::runtime:agent-analyzer")
    assert parsed == identifier


def test_parse_unique_identifier():
    parsed = ID.parse("workflow::manager:data-adapter<Index>")

    assert parsed == ID.workflow.manager.data.adapter.unique("Index")
    assert parsed.matches("workflow::manager:data-adapter")


def test_parse_role_without_component():
    parsed = ID.parse("system::runtime-analyzer")

    assert parsed == ID.system.runtime.analyzer
    assert parsed.component is None
    assert parsed.role is RoleNamespace.analyzer


def test_parse_group_only():
    parsed = ID.parse("system")

    assert parsed == ID.system
    assert parsed.source is None
    assert parsed.component is None
    assert parsed.role is None
    assert parsed.segment is parsed.group


def test_matches():
    identifier = ID.system.runtime.agent.analyzer
    assert identifier.matches(ID.system)
    assert identifier.matches(ID.system.runtime)
    assert identifier.matches(ID.system.runtime.agent)
    assert identifier.matches(ID.system.runtime.agent.analyzer)
    assert not identifier.matches(ID.service)


def test_parent():
    identifier = ID.system.runtime.agent.analyzer
    assert str(identifier.parent) == "system::runtime:agent"
    assert str(identifier.parent.parent) == "system::runtime"
    assert str(identifier.parent.parent.parent) == "system"


def test_parents_returns_full_hierarchy():
    identifier = ID.system.runtime.agent.analyzer

    assert tuple(str(parent) for parent in identifier.parents) == (
        "system::runtime:agent",
        "system::runtime",
        "system",
    )


def test_identifier_properties():
    identifier = ID.system.runtime.agent.analyzer

    assert identifier.parts == (
        identifier.group,
        identifier.source,
        identifier.component,
        identifier.role,
        None,
    )
    assert identifier.segment is identifier.role
    assert identifier.string_parts == ("system", "runtime", "agent", "analyzer")
    assert identifier.path == "system/runtime/agent/analyzer"
    assert identifier.slug == "system-runtime-agent-analyzer"
    assert identifier.metric_key == "system.runtime.agent.analyzer"
    assert identifier.cache_key == "system::runtime:agent-analyzer"
    assert identifier.event_topic == "system/runtime/agent/analyzer"
    assert identifier.has_role is True
    assert identifier.has_action is True


def test_identifier_to_dict():
    identifier = ID.system.runtime.agent.analyzer

    assert identifier.to_dict() == {
        "group": "system",
        "source": "runtime",
        "component": "agent",
        "role": "analyzer",
        "unique_id": None,
        "segment": "analyzer",
        "namespace": "system::runtime:agent",
        "qualified": "system::runtime:agent-analyzer",
        "path": "system/runtime/agent/analyzer",
        "slug": "system-runtime-agent-analyzer",
        "metric_key": "system.runtime.agent.analyzer",
        "cache_key": "system::runtime:agent-analyzer",
        "event_topic": "system/runtime/agent/analyzer",
        "value": "system::runtime:agent-analyzer",
    }


def test_unique_identifier_to_dict():
    identifier = ID.workflow.manager.data.adapter.unique("Index")

    assert identifier.to_dict() == {
        "group": "workflow",
        "source": "manager",
        "component": "data",
        "role": "adapter",
        "unique_id": "Index",
        "segment": "adapter",
        "namespace": "workflow::manager:data",
        "qualified": "workflow::manager:data-adapter<Index>",
        "path": "workflow/manager/data/adapter",
        "slug": "workflow-manager-data-adapter",
        "metric_key": "workflow.manager.data.adapter",
        "cache_key": "workflow::manager:data-adapter<Index>",
        "event_topic": "workflow/manager/data/adapter",
        "value": "workflow::manager:data-adapter<Index>",
    }


def test_identifier_segment_falls_back_to_previous_segment():
    assert (
        ID.system.runtime.agent.analyzer.segment
        is ID.system.runtime.agent.analyzer.role
    )
    assert ID.system.runtime.agent.segment is ID.system.runtime.agent.component
    assert ID.system.runtime.segment is ID.system.runtime.source
    assert ID.system.segment is ID.system.group


@pytest.mark.parametrize(
    ("identifier", "expected_segment", "expected_namespace", "expected_value"),
    [
        (ID.system, "system", "system", "system"),
        (ID.system.runtime, "runtime", "system::runtime", "system::runtime"),
        (
            ID.system.runtime.agent,
            "agent",
            "system::runtime:agent",
            "system::runtime:agent",
        ),
        (
            ID.system.runtime.agent.analyzer,
            "analyzer",
            "system::runtime:agent",
            "system::runtime:agent-analyzer",
        ),
    ],
)
def test_partial_identities_serialize_with_segment_fallback(
    identifier: Identifier,
    expected_segment: str,
    expected_namespace: str,
    expected_value: str,
):
    assert identifier.segment.value == expected_segment
    assert identifier.namespace == expected_namespace
    assert identifier.qualified == expected_value
    assert identifier.value == expected_value
    assert identifier.to_dict()["segment"] == expected_segment


def test_matches_string_identifier():
    identifier = ID.system.runtime.agent.analyzer

    assert identifier.matches("system::runtime:agent")
    assert identifier.matches("system::runtime:agent-analyzer")
    assert not identifier.matches("service::runtime:agent-analyzer")
    assert not identifier.matches("not-an-identifier")


def test_unique_identifier_match_requires_unique_when_requested():
    identifier = ID.workflow.manager.data.adapter.unique("Index")

    assert identifier.matches("workflow::manager:data-adapter")
    assert identifier.matches("workflow::manager:data-adapter<Index>")
    assert not identifier.matches("workflow::manager:data-adapter<Other>")


def test_require_complete_raises_for_incomplete_identifier():
    with pytest.raises(IdentifierValidationError, match="requires an role"):
        ID.system.runtime.require_complete()


def test_require_action_is_alias_for_require_role():
    identifier = ID.system.runtime.agent.analyzer

    assert identifier.require_action() is identifier

    with pytest.raises(IdentifierValidationError, match="requires an role"):
        ID.system.runtime.require_action()


def test_duplicate_role_raises_validation_error():
    with pytest.raises(IdentifierValidationError, match="already has an role"):
        ID.system.runtime.agent.analyzer.runner


def test_unique_requires_role():
    with pytest.raises(
        IdentifierValidationError,
        match="Cannot set unique id before role",
    ):
        ID.workflow.manager.data.unique("Index")


def test_duplicate_unique_raises_validation_error():
    with pytest.raises(
        IdentifierValidationError,
        match="already has a unique id",
    ):
        ID.workflow.manager.data.adapter.unique("Index").unique("Other")


def test_component_without_source_raises_validation_error():
    with pytest.raises(
        IdentifierValidationError,
        match="Cannot set component before source",
    ):
        ID.system.with_component(ID.source.resource)


def test_parse_rejects_invalid_values():
    with pytest.raises(IdentifierParseError, match="Identifier cannot be empty"):
        ID.parse("")

    with pytest.raises(IdentifierParseError, match="Invalid group 'invalid'"):
        ID.parse("invalid::runtime:agent-analyzer")

    with pytest.raises(IdentifierParseError, match="Invalid source 'invalid'"):
        ID.parse("system::invalid:agent-analyzer")

    with pytest.raises(IdentifierParseError, match="Invalid role 'invalid'"):
        ID.parse("system::runtime:agent-invalid")

    with pytest.raises(IdentifierParseError, match="Unique id cannot be empty"):
        ID.parse("system::runtime:agent-analyzer<>")

    with pytest.raises(IdentifierParseError, match="Invalid role 'agent\\+analyzer'"):
        ID.parse("system::runtime-agent+analyzer")


def test_enum_group():
    assert GroupNamespace.account == "account"


def test_enum_source():
    assert SourceNamespace.knowledge == "knowledge"


def test_enum_role():
    assert RoleNamespace.orchestrator == "orchestrator"


def test_enum_operation():
    assert OperationNamespace.execute == "execute"


def test_package_root_exports_current_public_api():
    assert idkit.ID is ID
    assert idkit.Identifier is Identifier
    assert idkit.OperationIdentifier is OperationIdentifier
    assert idkit.IDLike is IDLike
    assert idkit.IDable is IDable
    assert idkit.Identity is Identity
    assert idkit.IdentityNamespace is IdentityNamespace
    assert idkit.IdentityLike is IdentityLike
    assert idkit.Identifiable is Identifiable
    assert idkit.IdentifierError is IdentifierError
    assert idkit.IdentifierParseError is IdentifierParseError
    assert idkit.IdentifierValidationError is IdentifierValidationError


def test_package_root_all_matches_exported_names():
    for name in idkit.__all__:
        assert hasattr(idkit, name), name


def test_identity_like_consumer_can_use_segment_without_optional_unwrap():
    def current_segment(identifier: IDLike) -> str:
        return identifier.segment.value

    assert current_segment(ID.system.runtime.agent.analyzer) == "analyzer"
    assert current_segment(ID.system.runtime.agent) == "agent"
    assert current_segment(ID.system.runtime) == "runtime"
    assert current_segment(ID.system) == "system"
