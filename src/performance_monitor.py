from __future__ import annotations

import random
import time
import tracemalloc
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

from src.brute_force import exhaustive_shortest_path
from src.data_structures import Adjacency, add_undirected_edge
from src.greedy import dijkstra_shortest_path


@dataclass
class PerformanceRecord:
    algorithm: str
    n: int
    time_ms: float
    memory_mb: float
    operations: int
    cost: float


def generate_connected_graph(n: int, extra_edges: int = 2, seed: int = 42) -> Adjacency:
    random.seed(seed + n)
    graph: Adjacency = {idx: [] for idx in range(n)}

    for idx in range(n - 1):
        add_undirected_edge(graph, idx, idx + 1, round(random.uniform(1.0, 9.0), 2))

    attempts = 0
    target_edges = n * extra_edges
    while attempts < target_edges:
        source = random.randrange(n)
        target = random.randrange(n)
        attempts += 1
        if source == target:
            continue
        if any(neighbor == target for neighbor, _ in graph[source]):
            continue
        add_undirected_edge(graph, source, target, round(random.uniform(1.0, 12.0), 2))

    return graph


def measure(label: str, n: int, fn: Callable[[], Tuple[float, int]]) -> PerformanceRecord:
    tracemalloc.start()
    start = time.perf_counter()
    cost, operations = fn()
    elapsed_ms = (time.perf_counter() - start) * 1000
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return PerformanceRecord(
        algorithm=label,
        n=n,
        time_ms=elapsed_ms,
        memory_mb=peak / (1024 * 1024),
        operations=operations,
        cost=cost,
    )


def run_benchmark(sizes: List[int] | None = None) -> List[PerformanceRecord]:
    sizes = sizes or [5, 8, 10, 12, 20, 50, 100]
    records: List[PerformanceRecord] = []

    for n in sizes:
        graph = generate_connected_graph(n)
        source, target = 0, n - 1

        if n <= 12:
            records.append(
                measure(
                    "Forca Bruta",
                    n,
                    lambda graph=graph, source=source, target=target: (
                        lambda result: (result.cost, result.recursive_calls)
                    )(exhaustive_shortest_path(graph, source, target)),
                )
            )

        records.append(
            measure(
                "Dijkstra Guloso",
                n,
                lambda graph=graph, source=source, target=target: (
                    lambda result: (result.cost, result.operations)
                )(dijkstra_shortest_path(graph, source, target)),
            )
        )

    return records
