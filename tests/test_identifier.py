import pytest

import idkit
from idkit.idkit import ID
from idkit.exceptions import IdentifierParseError, IdentifierValidationError


def test_identifier_value():
    identifier = ID.system.runtime.agent.analyzer
    assert str(identifier) == "system::runtime-agent+analyzer"
    assert identifier.value == "system::runtime-agent+analyzer"


def test_namespace():
    identifier = ID.system.runtime.agent.analyzer
    assert identifier.namespace == "system::runtime-agent"


def test_parse():
    identifier = ID.system.runtime.agent.analyzer
    parsed = ID.parse("system::runtime-agent+analyzer")
    assert parsed == identifier


def test_parse_group_only():
    parsed = ID.parse("system")

    assert parsed == ID.system
    assert parsed.source is None
    assert parsed.role is None


def test_matches():
    identifier = ID.system.runtime.agent.analyzer
    assert identifier.matches(ID.system)
    assert identifier.matches(ID.system.runtime)
    assert identifier.matches(ID.system.runtime.agent)
    assert identifier.matches(ID.system.runtime.agent.analyzer)
    assert not identifier.matches(ID.service)


def test_parent():
    identifier = ID.system.runtime.agent.analyzer
    assert str(identifier.parent) == "system::runtime-agent"
    assert str(identifier.parent.parent) == "system::runtime"
    assert str(identifier.parent.parent.parent) == "system"


def test_parents_returns_full_hierarchy():
    identifier = ID.system.runtime.agent.analyzer

    assert tuple(str(parent) for parent in identifier.parents) == (
        "system::runtime-agent",
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
    )
    assert identifier.string_parts == ("system", "runtime", "agent", "analyzer")
    assert identifier.path == "system/runtime/agent/analyzer"
    assert identifier.slug == "system-runtime-agent-analyzer"
    assert identifier.metric_key == "system.runtime.agent.analyzer"
    assert identifier.cache_key == "system::runtime-agent+analyzer"
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
        "namespace": "system::runtime-agent",
        "qualified": "system::runtime-agent+analyzer",
        "path": "system/runtime/agent/analyzer",
        "slug": "system-runtime-agent-analyzer",
        "metric_key": "system.runtime.agent.analyzer",
        "cache_key": "system::runtime-agent+analyzer",
        "event_topic": "system/runtime/agent/analyzer",
        "value": "system::runtime-agent+analyzer",
    }


def test_matches_string_identifier():
    identifier = ID.system.runtime.agent.analyzer

    assert identifier.matches("system::runtime-agent")
    assert identifier.matches("system::runtime-agent+analyzer")
    assert not identifier.matches("service::runtime-agent+analyzer")
    assert not identifier.matches("not-an-identifier")


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
        ID.parse("invalid::runtime-agent+analyzer")

    with pytest.raises(IdentifierParseError, match="Invalid source 'invalid'"):
        ID.parse("system::invalid-agent+analyzer")

    with pytest.raises(IdentifierParseError, match="Invalid role 'invalid'"):
        ID.parse("system::runtime-agent+invalid")


def test_enum_group():
    from idkit import IdentifierGroup

    assert IdentifierGroup.account == "account"


def test_enum_source():
    from idkit import IdentifierSource

    assert IdentifierSource.knowledge == "knowledge"


def test_enum_role():
    from idkit import IdentifierRole

    assert IdentifierRole.orchestrator == "orchestrator"


def test_enum_operation():
    from idkit import IdentifierOperation

    assert IdentifierOperation.execute == "execute"


def test_package_root_exports_documented_aliases():
    assert hasattr(idkit, "AppIdentifier")
    assert hasattr(idkit, "AppIdentifierRoot")
    assert hasattr(idkit, "AppIdentifierLike")
    assert hasattr(idkit, "AppIdentifiable")
    assert hasattr(idkit, "IDKitIdentifier")
    assert hasattr(idkit, "IDKitIdentifierRoot")
    assert hasattr(idkit, "IDKitIdentifierLike")
    assert hasattr(idkit, "IDKitIdentifiable")
