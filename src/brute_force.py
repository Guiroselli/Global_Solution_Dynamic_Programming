from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from src.data_structures import Adjacency


@dataclass
class BruteForceResult:
    path: List[int]
    cost: float
    recursive_calls: int
    paths_evaluated: int
    all_costs: List[float]


def exhaustive_shortest_path(graph: Adjacency, source: int, target: int) -> BruteForceResult:
    best_path: List[int] = []
    best_cost = float("inf")
    recursive_calls = 0
    paths_evaluated = 0
    all_costs: List[float] = []

    def backtrack(current: int, visited: set[int], path: List[int], cost: float) -> None:
        nonlocal best_path, best_cost, recursive_calls, paths_evaluated
        recursive_calls += 1

        if current == target:
            paths_evaluated += 1
            all_costs.append(cost)
            if cost < best_cost:
                best_cost = cost
                best_path = path.copy()
            return

        for neighbor, weight in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                backtrack(neighbor, visited, path, cost + weight)
                path.pop()
                visited.remove(neighbor)

    backtrack(source, {source}, [source], 0.0)
    return BruteForceResult(
        path=best_path,
        cost=best_cost,
        recursive_calls=recursive_calls,
        paths_evaluated=paths_evaluated,
        all_costs=all_costs,
    )
