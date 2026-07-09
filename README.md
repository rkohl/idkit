# IDKit

A small typed identifier system for Python 3.12+.

It lets you build structured identifiers using dot notation:

```python
from idkit import ID

identifier = ID.system.runtime.agent.analyzer

print(identifier)
# system::runtime:agent-analyzer

print(identifier.namespace)
# system::runtime:agent

print(identifier.segment)
# analyzer

print(identifier.path)
# system/runtime/agent/analyzer

print(identifier.slug)
# system-runtime-agent-analyzer

print(identifier.unique("worker-1"))
# system::runtime:agent-analyzer<worker-1>
```

## Format

```text
Group::Source[:Component][-Role][<Unique>]
```

Examples:

```text
system::runtime
system::runtime
system::runtime:agent
system::runtime:agent-analyzer
system::runtime:agent-analyzer<worker-1>
service::data:resource-ingester
manage::workflow:pipeline-runner
```

## Type aliases

```python
from idkit import Identifier, IDLike, IDable
```

Use `Identifier` when you want the concrete identity type.

Use `IDLike` when your function only needs the public identity interface.

Use `IDable` when your object exposes an `.identifier` property.

The root package also exports the generic building blocks:

```python
from idkit import Identity, IdentityLike, Identifiable, IdentityNamespace
```

```python
from idkit import IDLike


def register(identifier: IDLike) -> None:
    identifier.require_complete()
    print(identifier.value)
```

## Installation

```bash
pip install idkit
```

## Parsing

```python
parsed = ID.parse("system::runtime:agent-analyzer")

assert parsed == ID.system.runtime.agent.analyzer

unique = ID.parse("system::runtime:agent-analyzer<worker-1>")

assert unique == ID.system.runtime.agent.analyzer.unique("worker-1")
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
# Identifier('system::runtime:agent')

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
