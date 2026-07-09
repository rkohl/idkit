# IDKit

A small typed identifier system for Python 3.12+.

It lets you build structured identifiers using dot notation:

```python
from idkit import ID

identifier = ID.system.runtime.agent.analyzer

print(identifier)
# system::runtime-agent+analyzer

print(identifier.namespace)
# system::runtime-agent

print(identifier.segment)
# analyzer

print(identifier.path)
# system/runtime/agent/analyzer

print(identifier.slug)
# system-runtime-agent-analyzer
```

## Format

```text
Group::Source[-Component][+Role]
```

Examples:

```text
system::runtime
system::runtime-agent
system::runtime-agent+analyzer
service::data-resource+ingester
manage::workflow-pipeline+runner
```

## Type aliases

```python
from idkit import IDKitIdentifier, IDKitIdentifierLike, IDKitIdentifiable
```

Use `IDKitIdentifier` when you want the concrete implementation.

Use `IDKitIdentifierLike` when your function only needs the public identifier interface.

Use `IDKitIdentifiable` when your object exposes an `.identifier` property.

Compatibility aliases are also exported:

```python
from idkit import IDKitIdentifier, IDKitIdentifierLike, IDKitIdentifiable
```

```python
def register(identifier: IDKitIdentifierLike) -> None:
    identifier.require_complete()
    print(identifier.value)
```

## Installation

```bash
pip install idkit
```

## Parsing

```python
parsed = ID.parse("system::runtime-agent+analyzer")

assert parsed == ID.system.runtime.agent.analyzer
```

## Matching

```python
identifier = ID.system.runtime.agent.analyzer

identifier.matches(ID.system)
# True

identifier.matches(ID.system.runtime)
# True

identifier.matches(ID.system.runtime.agent)
# True

identifier.matches(ID.service)
# False
```

## Parent traversal

```python
identifier = ID.system.runtime.agent.analyzer

identifier.parent
# Identifier('system::runtime-agent')

identifier.parent.parent
# Identifier('system::runtime')

identifier.parent.parent.parent
# Identifier('system')
```

## Development

Run tests:

```bash
python3 -m pytest
```
