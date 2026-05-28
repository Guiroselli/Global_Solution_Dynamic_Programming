from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

Municipality = Tuple[int, str, float, float, int]
Adjacency = Dict[int, List[Tuple[int, float]]]


@dataclass
class Node:
    municipality: Municipality
    left: Optional["Node"] = None
    right: Optional["Node"] = None

    @property
    def key(self) -> Tuple[float, int]:
        return (self.municipality[2], self.municipality[0])


class BinarySearchTree:
    def __init__(self) -> None:
        self.root: Optional[Node] = None

    def insert(self, municipality: Municipality) -> None:
        self.root = self._insert(self.root, municipality)

    def _insert(self, node: Optional[Node], municipality: Municipality) -> Node:
        if node is None:
            return Node(municipality)

        new_key = (municipality[2], municipality[0])
        if new_key < node.key:
            node.left = self._insert(node.left, municipality)
        else:
            node.right = self._insert(node.right, municipality)
        return node

    def search_range(self, risk_min: float, risk_max: float) -> List[Municipality]:
        found: List[Municipality] = []
        self._search_range(self.root, risk_min, risk_max, found)
        return found

    def _search_range(
        self,
        node: Optional[Node],
        risk_min: float,
        risk_max: float,
        found: List[Municipality],
    ) -> None:
        if node is None:
            return

        risk = node.municipality[2]
        if risk > risk_min:
            self._search_range(node.left, risk_min, risk_max, found)
        if risk_min <= risk <= risk_max:
            found.append(node.municipality)
        if risk < risk_max:
            self._search_range(node.right, risk_min, risk_max, found)

    def in_order(self) -> List[Municipality]:
        ordered: List[Municipality] = []
        self._in_order(self.root, ordered)
        return ordered

    def _in_order(self, node: Optional[Node], ordered: List[Municipality]) -> None:
        if node is None:
            return
        self._in_order(node.left, ordered)
        ordered.append(node.municipality)
        self._in_order(node.right, ordered)

    def height(self) -> int:
        return self._height(self.root)

    def _height(self, node: Optional[Node]) -> int:
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def remove(self, municipality_id: int) -> None:
        target = self._find_by_id(self.root, municipality_id)
        if target is not None:
            self.root = self._remove_by_key(self.root, target.key)

    def _find_by_id(self, node: Optional[Node], municipality_id: int) -> Optional[Node]:
        if node is None:
            return None
        if node.municipality[0] == municipality_id:
            return node
        return self._find_by_id(node.left, municipality_id) or self._find_by_id(
            node.right, municipality_id
        )

    def _remove_by_key(self, node: Optional[Node], key: Tuple[float, int]) -> Optional[Node]:
        if node is None:
            return None
        if key < node.key:
            node.left = self._remove_by_key(node.left, key)
            return node
        if key > node.key:
            node.right = self._remove_by_key(node.right, key)
            return node

        if node.left is None:
            return node.right
        if node.right is None:
            return node.left

        successor = self._min_node(node.right)
        node.municipality = successor.municipality
        node.right = self._remove_by_key(node.right, successor.key)
        return node

    def _min_node(self, node: Node) -> Node:
        current = node
        while current.left is not None:
            current = current.left
        return current


def add_undirected_edge(graph: Adjacency, source: int, target: int, weight: float) -> None:
    graph.setdefault(source, []).append((target, weight))
    graph.setdefault(target, []).append((source, weight))


def build_bst(municipalities: Iterable[Municipality]) -> BinarySearchTree:
    bst = BinarySearchTree()
    for municipality in municipalities:
        bst.insert(municipality)
    return bst


def bfs(graph: Adjacency, start: int) -> List[int]:
    visited = {start}
    order: List[int] = []
    queue: deque[int] = deque([start])

    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbor, _ in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def get_scenario_data(scenario: str = "rs") -> Tuple[List[Municipality], Adjacency]:
    if scenario == "matopiba":
        municipalities: List[Municipality] = [
            (2100055, "Acailandia", 0.68, 1250.0, 113121),
            (2105302, "Imperatriz", 0.74, 1320.0, 259980),
            (1721000, "Palmas", 0.61, 1180.0, 302692),
            (1702109, "Araguaina", 0.81, 1460.0, 183381),
            (2207702, "Parnaiba", 0.58, 980.0, 153482),
            (2211001, "Teresina", 0.70, 1410.0, 868075),
            (2903201, "Barreiras", 0.86, 1730.0, 158432),
            (2919553, "Luis Eduardo Magalhaes", 0.79, 1660.0, 107909),
        ]
        edges = [
            (2100055, 2105302, 1.2),
            (2105302, 1702109, 5.7),
            (1702109, 1721000, 4.9),
            (1721000, 2919553, 8.4),
            (2919553, 2903201, 1.4),
            (2207702, 2211001, 5.2),
            (2211001, 2105302, 8.9),
            (2211001, 2903201, 9.1),
            (1702109, 2919553, 7.6),
        ]
    else:
        municipalities = [
            (4314902, "Porto Alegre", 0.72, 1850.0, 1400000),
            (4304606, "Canoas", 0.89, 920.0, 347657),
            (4318705, "Sao Leopoldo", 0.78, 760.0, 240378),
            (4320008, "Sapucaia do Sul", 0.80, 690.0, 141808),
            (4309209, "Gravatai", 0.66, 840.0, 265070),
            (4303103, "Cachoeirinha", 0.63, 640.0, 131240),
            (4313375, "Nova Santa Rita", 0.84, 710.0, 29712),
            (4306767, "Eldorado do Sul", 0.91, 870.0, 41771),
            (4313409, "Novo Hamburgo", 0.73, 930.0, 247032),
            (4307708, "Esteio", 0.82, 580.0, 84237),
        ]
        edges = [
            (4314902, 4304606, 0.6),
            (4314902, 4303103, 0.7),
            (4314902, 4306767, 0.5),
            (4304606, 4313375, 0.8),
            (4304606, 4307708, 0.4),
            (4307708, 4320008, 0.3),
            (4320008, 4318705, 0.4),
            (4318705, 4313409, 0.6),
            (4303103, 4309209, 0.4),
            (4309209, 4313409, 1.1),
            (4313375, 4306767, 1.0),
            (4313375, 4318705, 1.2),
        ]

    graph: Adjacency = {municipality[0]: [] for municipality in municipalities}
    for source, target, weight in edges:
        add_undirected_edge(graph, source, target, weight)
    return municipalities, graph


def municipality_lookup(municipalities: Iterable[Municipality]) -> Dict[int, Municipality]:
    return {municipality[0]: municipality for municipality in municipalities}
