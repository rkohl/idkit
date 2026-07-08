from idkit import ID, IDKitIdentifier, IDKitIdentifierLike


def register(identifier: IDKitIdentifierLike) -> None:
    identifier.require_complete()
    print(f"Registering: {identifier.value}")


identifier: IDKitIdentifier = ID.system.runtime.agent.analyzer

print(identifier)
print(identifier.namespace)
print(identifier.path)
print(identifier.slug)
print(identifier.metric_key)
print(identifier.to_dict())

register(identifier)

parsed = ID.parse("system::runtime-agent+analyzer")

assert parsed == identifier
assert parsed == "system::runtime-agent+analyzer"

assert identifier.matches(ID.system)
assert identifier.matches(ID.system.runtime)
assert identifier.matches(ID.system.runtime.agent)
assert not identifier.matches(ID.service)

print(identifier.parent)
print(identifier.parents)
