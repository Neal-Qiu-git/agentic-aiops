# ADR-002: Why MCP (Model Context Protocol)

## Status

Accepted

## Context

We need a standard way for agents to call external tools. The solution must:
1. Support multiple tool types (SSH, K8s, Docker, DB, etc.)
2. Allow easy plugin development
3. Be language-agnostic
4. Support tool discovery and description

## Decision

We adopt **MCP (Model Context Protocol)** as our tool interface standard.

### Why MCP?

1. **Standardization** — Common protocol for tool invocation
2. **Extensibility** — Easy to add new tools
3. **Discoverability** — Tools can be introspected
4. **Language Agnostic** — Works with any LLM provider

### Architecture

```
Agent
  │
  ▼
MCP Client
  │
  ▼
MCP Server (Tool Registry)
  │
  ├── SSH Tool
  ├── K8s Tool
  ├── Docker Tool
  ├── MySQL Tool
  ├── Redis Tool
  └── ...
```

### Alternatives Considered

| Approach | Pros | Cons | Why Not |
|----------|------|------|---------|
| Direct API calls | Simple | Tight coupling | Cannot swap tools |
| Function calling (OpenAI) | Native | Provider lock-in | Not portable |
| Custom protocol | Flexible | No ecosystem | Reinventing wheel |

## Consequences

### Positive
- Standard tool interface
- Easy to create plugins
- Can share tools across agents
- Supports tool composition

### Negative
- Additional abstraction layer
- Need to maintain MCP compatibility

## References

- [MCP Specification](https://modelcontextprotocol.io/)
- [Anthropic MCP](https://github.com/modelcontextprotocol)
