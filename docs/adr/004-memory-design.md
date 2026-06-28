# ADR-004: Memory System Design

## Status

Accepted

## Context

Operations agents need to learn from past incidents. The memory system must:
1. Store operational experiences
2. Retrieve similar past incidents
3. Support different types of memories
4. Persist across sessions

## Decision

We implement a **5-type memory system**.

### Memory Types

| Type | Storage | TTL | Use Case |
|------|---------|-----|----------|
| Working | RAM | Session | Current task context |
| Short-term | RAM | 1 hour | Recent interactions |
| Long-term | File | Permanent | Important experiences |
| Semantic | Vector DB | Permanent | Similar incident search |
| Episodic | File | Permanent | Specific events |

### Why 5 Types?

1. **Working** — Fast access for current context
2. **Short-term** — Retains recent conversation
3. **Long-term** — Preserves important learnings
4. **Semantic** — Enables similarity search
5. **Episodic** — Records specific incidents

### Memory Flow

```
Incident Occurs
       │
       ▼
Agent Diagnoses
       │
       ▼
Record to Working Memory
       │
       ▼
After Resolution
       │
       ▼
Promote to Long-term Memory
       │
       ▼
Generate Embedding
       │
       ▼
Store in Semantic Memory
       │
       ▼
Next Similar Incident
       │
       ▼
Retrieve from Semantic Memory
```

### Embedding Strategy

- Use local embeddings for small deployments
- Support vector databases (Chroma, Pinecone) for scale
- Hybrid search: keyword + semantic

### Alternatives Considered

| Approach | Pros | Cons | Why Not |
|----------|------|------|---------|
| Simple key-value | Simple | No semantic search | Cannot find similar |
| Single vector DB | Unified | Complex | Overkill for small scale |
| External service | Scalable | Dependency | Not self-contained |

## Consequences

### Positive
- Comprehensive memory coverage
- Supports operational learning
- Can find similar past incidents
- Self-contained deployment

### Negative
- More storage requirements
- Need embedding generation
- Complexity in memory management

## References

- [MemGPT](https://github.com/cpacker/MemGPT)
- [LangChain Memory](https://python.langchain.com/docs/modules/memory/)
