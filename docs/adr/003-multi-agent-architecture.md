# ADR-003: Multi-Agent Architecture

## Status

Accepted

## Context

Operations tasks span multiple domains (Linux, K8s, DB, Monitoring). A single agent cannot be an expert in all areas. We need:
1. Specialized agents for each domain
2. A way to coordinate multiple agents
3. Task decomposition and result aggregation

## Decision

We adopt a **Planner + Specialist Agents** architecture.

### Architecture

```
User Request
      │
      ▼
Planner Agent
      │
      ├──▶ Linux Agent
      ├──▶ K8s Agent
      ├──▶ DB Agent
      ├──▶ Log Agent
      ├──▶ Monitor Agent
      └──▶ Security Agent
              │
              ▼
      Result Aggregation
```

### Why Multi-Agent?

1. **Specialization** — Each agent focuses on one domain
2. **Parallelism** — Multiple agents can work simultaneously
3. **Maintainability** — Easier to update individual agents
4. **Scalability** — Can add new agents without changing existing ones

### Agent Communication

Agents communicate through:
1. **Event Bus** — Asynchronous messaging
2. **Shared Context** — Common memory space
3. **Planner Coordination** — Central orchestration

### Alternatives Considered

| Approach | Pros | Cons | Why Not |
|----------|------|------|---------|
| Single agent | Simple | Too complex for one agent | Cannot master all domains |
| Peer-to-peer | Decentralized | Hard to coordinate | Chaos in large systems |
| Hierarchical | Clear structure | Single point of failure | Planner is critical |

## Consequences

### Positive
- Clear separation of concerns
- Easy to test individual agents
- Can scale horizontally
- Domain expertise preserved

### Negative
- More complex than single agent
- Need coordination logic
- Potential for conflicting actions

## References

- [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)
- [AutoGen Architecture](https://github.com/microsoft/autogen)
- [CrewAI Architecture](https://github.com/joaomdmoura/crewAI)
