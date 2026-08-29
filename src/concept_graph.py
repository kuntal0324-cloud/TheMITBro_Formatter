from __future__ import annotations
from dataclasses import dataclass
from .question_taxonomy import NODES

@dataclass(frozen=True)
class ConceptEdge:
    prerequisite: str
    concept: str

def build_concept_graph() -> dict[str, tuple[str, ...]]:
    graph: dict[str, set[str]] = {}
    for node in NODES:
        graph.setdefault(node.concept, set())
        for pre in node.prerequisites:
            graph[node.concept].add(pre)
            graph.setdefault(pre, set())
    return {k: tuple(sorted(v)) for k,v in sorted(graph.items())}

def prerequisites_for(concept: str, *, transitive: bool=False) -> tuple[str, ...]:
    graph=build_concept_graph()
    direct=graph.get(concept, ())
    if not transitive:
        return direct
    seen=set()
    stack=list(direct)
    while stack:
        x=stack.pop()
        if x in seen: continue
        seen.add(x)
        stack.extend(graph.get(x, ()))
    return tuple(sorted(seen))

def validate_acyclic() -> bool:
    graph=build_concept_graph()
    visiting=set(); visited=set()
    def dfs(n):
        if n in visiting: return False
        if n in visited: return True
        visiting.add(n)
        for p in graph.get(n,()):
            if not dfs(p): return False
        visiting.remove(n); visited.add(n); return True
    return all(dfs(n) for n in graph)
