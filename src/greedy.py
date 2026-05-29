from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from src.data_structures import Adjacency


@dataclass
class DijkstraResult:
    path: List[int]
    cost: float
    distances: Dict[int, float]
    predecessors: Dict[int, Optional[int]]
    operations: int
    heap_pushes: int


def dijkstra_shortest_path(graph: Adjacency, source: int, target: int) -> DijkstraResult:
    distances = {node: float("inf") for node in graph}
    predecessors: Dict[int, Optional[int]] = {node: None for node in graph}
    distances[source] = 0.0
    heap: List[Tuple[float, int]] = [(0.0, source)]
    visited: set[int] = set()
    operations = 0
    heap_pushes = 1

    while heap:
        current_distance, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)

        if current == target:
            break

        for neighbor, weight in graph.get(current, []):
            operations += 1
            candidate = current_distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                predecessors[neighbor] = current
                heapq.heappush(heap, (candidate, neighbor))
                heap_pushes += 1

    path = reconstruct_path(predecessors, source, target)
    return DijkstraResult(
        path=path,
        cost=distances[target],
        distances=distances,
        predecessors=predecessors,
        operations=operations,
        heap_pushes=heap_pushes,
    )


def reconstruct_path(
    predecessors: Dict[int, Optional[int]], source: int, target: int
) -> List[int]:
    if source == target:
        return [source]
    if predecessors.get(target) is None:
        return []

    path = [target]
    current = target
    while current != source:
        previous = predecessors[current]
        if previous is None:
            return []
        path.append(previous)
        current = previous
    path.reverse()
    return path


@dataclass
class PrimResult:
    edges: List[Tuple[int, int, float]]
    total_cost: float
    heap_pushes: int


def prim_mst(graph: Adjacency, start: int) -> PrimResult:
    visited = {start}
    heap: List[Tuple[float, int, int]] = []
    heap_pushes = 0
    for neighbor, weight in graph.get(start, []):
        heapq.heappush(heap, (weight, start, neighbor))
        heap_pushes += 1

    mst_edges: List[Tuple[int, int, float]] = []
    total_cost = 0.0

    while heap and len(visited) < len(graph):
        weight, source, target = heapq.heappop(heap)
        if target in visited:
            continue
        visited.add(target)
        mst_edges.append((source, target, weight))
        total_cost += weight

        for neighbor, next_weight in graph.get(target, []):
            if neighbor not in visited:
                heapq.heappush(heap, (next_weight, target, neighbor))
                heap_pushes += 1

    return PrimResult(edges=mst_edges, total_cost=total_cost, heap_pushes=heap_pushes)
