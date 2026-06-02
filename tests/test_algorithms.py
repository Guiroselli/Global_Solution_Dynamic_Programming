from src.brute_force import exhaustive_shortest_path
from src.data_structures import build_bst, get_scenario_data
from src.greedy import dijkstra_shortest_path, prim_mst


def test_bst_orders_and_filters_by_risk() -> None:
    municipalities, _ = get_scenario_data("rs")
    bst = build_bst(municipalities)

    ordered_risks = [municipality[2] for municipality in bst.in_order()]
    high_risk = bst.search_range(0.80, 1.00)

    assert ordered_risks == sorted(ordered_risks)
    assert all(municipality[2] >= 0.80 for municipality in high_risk)
    assert bst.height() > 0


def test_bst_remove_by_id() -> None:
    municipalities, _ = get_scenario_data("rs")
    bst = build_bst(municipalities)
    removed_id = municipalities[0][0]

    bst.remove(removed_id)

    assert removed_id not in [municipality[0] for municipality in bst.in_order()]


def test_dijkstra_matches_brute_force_on_small_graph() -> None:
    _, graph = get_scenario_data("rs")
    source = 4314902
    target = 4306767

    brute = exhaustive_shortest_path(graph, source, target)
    greedy = dijkstra_shortest_path(graph, source, target)

    assert greedy.path == brute.path
    assert greedy.cost == brute.cost


def test_prim_returns_spanning_tree() -> None:
    _, graph = get_scenario_data("matopiba")
    result = prim_mst(graph, next(iter(graph)))

    assert len(result.edges) == len(graph) - 1
    assert result.total_cost > 0
