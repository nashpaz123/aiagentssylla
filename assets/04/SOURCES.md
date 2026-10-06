# Session 4 diagram sources

All seven slides are **course-generated** educational diagrams (`scripts/gen_diagrams.py` → `s04_*`), redesigned for density:

| Asset | What it teaches |
|---|---|
| `01-langgraph-hero.png` | Full support-agent StateGraph (State sidebar, loop, HITL, END) |
| `02-graph-basics.png` | Café pipeline + Node / Edge / Directed vocabulary cards |
| `03-shared-state.png` | Field ownership, Reducer bug, merge rules |
| `04-conditional-edges.png` | `should_continue` → tools / hitl / end |
| `05-checkpoint.png` | Super-step timeline, thread_id, checkpointer choices |
| `06-hitl-interrupt.png` | interrupt → UI → resume + policy examples |
| `07-agent-tools-loop.png` | Session-3 Function Calling mapped into graph nodes |

Regenerate:

```bash
python3 -c "from scripts import gen_diagrams as g; [f() for f in (g.s04_hero,g.s04_graph_basics,g.s04_state,g.s04_conditional,g.s04_checkpoint,g.s04_hitl,g.s04_agent_loop)]"
```
