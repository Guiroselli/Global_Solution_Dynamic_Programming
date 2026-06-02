from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import matplotlib.pyplot as plt
import networkx as nx

from src.data_structures import Adjacency, BinarySearchTree, Municipality, Node
from src.greedy import prim_mst
from src.performance_monitor import PerformanceRecord


def ensure_output_dir(path: str | Path = "report/figures") -> Path:
    output = Path(path)
    output.mkdir(parents=True, exist_ok=True)
    return output


def plot_graph_with_mst(
    graph: Adjacency,
    municipalities: Iterable[Municipality],
    output_path: str | Path,
) -> None:
    lookup = {municipality[0]: municipality[1] for municipality in municipalities}
    nx_graph = nx.Graph()
    for source, neighbors in graph.items():
        for target, weight in neighbors:
            if source < target:
                nx_graph.add_edge(source, target, weight=weight)

    mst = prim_mst(graph, next(iter(graph)))
    mst_pairs = {tuple(sorted((source, target))) for source, target, _ in mst.edges}
    edge_colors = [
        "#d62828" if tuple(sorted(edge)) in mst_pairs else "#8d99ae"
        for edge in nx_graph.edges()
    ]
    edge_widths = [2.8 if tuple(sorted(edge)) in mst_pairs else 1.2 for edge in nx_graph.edges()]

    plt.figure(figsize=(10, 7))
    position = nx.spring_layout(nx_graph, seed=7)
    nx.draw_networkx_nodes(nx_graph, position, node_color="#edf2f4", edgecolors="#2b2d42")
    nx.draw_networkx_edges(nx_graph, position, edge_color=edge_colors, width=edge_widths)
    nx.draw_networkx_labels(
        nx_graph,
        position,
        labels={node: lookup.get(node, str(node)) for node in nx_graph.nodes()},
        font_size=8,
    )
    nx.draw_networkx_edge_labels(
        nx_graph,
        position,
        edge_labels=nx.get_edge_attributes(nx_graph, "weight"),
        font_size=7,
    )
    plt.title("Grafo de municipios com MST destacada")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()


def plot_bst(bst: BinarySearchTree, output_path: str | Path) -> None:
    positions: Dict[Tuple[float, int], Tuple[float, float]] = {}
    labels: Dict[Tuple[float, int], str] = {}
    edges: List[Tuple[Tuple[float, int], Tuple[float, int]]] = []

    def walk(node: Node | None, depth: int, x_min: float, x_max: float) -> None:
        if node is None:
            return
        x = (x_min + x_max) / 2
        y = -depth
        positions[node.key] = (x, y)
        labels[node.key] = f"{node.municipality[1]}\nrisco={node.municipality[2]:.2f}"
        for child, child_min, child_max in (
            (node.left, x_min, x),
            (node.right, x, x_max),
        ):
            if child is not None:
                edges.append((node.key, child.key))
                walk(child, depth + 1, child_min, child_max)

    walk(bst.root, 0, 0.0, 1.0)

    plt.figure(figsize=(12, 6))
    for source, target in edges:
        x1, y1 = positions[source]
        x2, y2 = positions[target]
        plt.plot([x1, x2], [y1, y2], color="#6c757d", linewidth=1.4)
    for key, (x, y) in positions.items():
        plt.scatter([x], [y], s=1800, color="#f1faee", edgecolor="#1d3557", zorder=3)
        plt.text(x, y, labels[key], ha="center", va="center", fontsize=8, zorder=4)
    plt.title("BST de municipios ordenada por indice de risco")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()


def plot_performance(records: List[PerformanceRecord], output_path: str | Path) -> None:
    plt.figure(figsize=(9, 5))
    for algorithm in sorted({record.algorithm for record in records}):
        data = [record for record in records if record.algorithm == algorithm]
        plt.plot(
            [record.n for record in data],
            [record.time_ms for record in data],
            marker="o",
            label=algorithm,
        )
    plt.title("Tempo de execucao por tamanho da instancia")
    plt.xlabel("Numero de vertices (N)")
    plt.ylabel("Tempo (ms)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()


def plot_optimality_gap(records: List[PerformanceRecord], output_path: str | Path) -> None:
    by_n: Dict[int, Dict[str, PerformanceRecord]] = {}
    for record in records:
        by_n.setdefault(record.n, {})[record.algorithm] = record

    x_values: List[int] = []
    gaps: List[float] = []
    for n, algorithms in sorted(by_n.items()):
        brute = algorithms.get("Forca Bruta")
        greedy = algorithms.get("Dijkstra Guloso")
        if brute and greedy and brute.cost > 0:
            x_values.append(n)
            gaps.append(((greedy.cost - brute.cost) / brute.cost) * 100)

    plt.figure(figsize=(8, 4.5))
    plt.axhline(0, color="#1d3557", linewidth=1.2)
    plt.bar(x_values, gaps, color="#457b9d", alpha=0.75)
    plt.scatter(x_values, gaps, color="#d62828", zorder=3)
    for x_value, gap in zip(x_values, gaps):
        plt.text(x_value, gap + 0.08, f"{gap:.1f}%", ha="center", va="bottom", fontsize=9)
    plt.title("Gap de otimalidade: Dijkstra vs Forca Bruta")
    plt.xlabel("Numero de vertices (N)")
    plt.ylabel("Gap percentual (%)")
    if gaps and max(gaps) == min(gaps) == 0:
        plt.ylim(-0.5, 1.0)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()
