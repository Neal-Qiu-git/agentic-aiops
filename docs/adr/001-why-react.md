# ADR-001: Why ReAct Pattern

## Status

Accepted

## Context

We need to choose a reasoning pattern for our AI operations agents. The agent must be able to:
1. Understand operational context
2. Make decisions based on observations
3. Execute actions
4. Verify results
5. Learn from outcomes

## Decision

We adopt the **ReAct (Reasoning + Acting)** pattern.

### ReAct Flow

```
Thought → Action → Observation → Thought → Action → ... → Final Answer
```

### Why ReAct?

1. **Transparency** — Every step is visible and auditable
2. **Debuggability** — Can trace exactly why a decision was made
3. **Controllability** — Human can interrupt at any step
4. **Verifiability** — Results can be checked before proceeding

### Alternatives Considered

| Pattern | Pros | Cons | Why Not |
|---------|------|------|---------|
| Chain-of-Thought | Simple | No action execution | Cannot perform operations |
| Plan-and-Execute | Good planning | No real-time adjustment | Too rigid for ops |
| Reflexion | Good learning | Complex | Overkill for v1 |

## Consequences

### Positive
- Clear reasoning chain
- Easy to implement approval gates
- Natural fit for operations workflows

### Negative
- Requires multiple LLM calls per task
- Can be slower than direct execution

## References

- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [LangChain ReAct](https://python.langchain.com/docs/modules/agents/agent_types/react)
