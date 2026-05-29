from __future__ import annotations

import csv
from pathlib import Path

from src.brute_force import exhaustive_shortest_path
from src.data_structures import build_bst, get_scenario_data, municipality_lookup
from src.greedy import dijkstra_shortest_path, prim_mst
from src.performance_monitor import run_benchmark
from src.visualizations import (
    ensure_output_dir,
    plot_bst,
    plot_graph_with_mst,
    plot_optimality_gap,
    plot_performance,
)


def run_scenario(scenario: str, source: int, risk_min: float, output_dir: Path) -> dict[str, object]:
    municipalities, graph = get_scenario_data(scenario)
    lookup = municipality_lookup(municipalities)
    bst = build_bst(municipalities)

    high_risk = bst.search_range(risk_min, 1.00)
    target = max(high_risk, key=lambda municipality: municipality[2])[0]

    brute = exhaustive_shortest_path(graph, source, target)
    greedy = dijkstra_shortest_path(graph, source, target)
    mst = prim_mst(graph, source)

    plot_graph_with_mst(graph, municipalities, output_dir / f"grafo_mst_{scenario}.png")
    plot_bst(bst, output_dir / f"bst_risco_{scenario}.png")

    return {
        "scenario": scenario,
        "high_risk": [item[1] for item in high_risk],
        "source": lookup[source][1],
        "target": lookup[target][1],
        "brute_path": " -> ".join(lookup[node][1] for node in brute.path),
        "brute_cost": brute.cost,
        "brute_calls": brute.recursive_calls,
        "greedy_path": " -> ".join(lookup[node][1] for node in greedy.path),
        "greedy_cost": greedy.cost,
        "greedy_operations": greedy.operations,
        "mst_cost": mst.total_cost,
        "mst_edges": len(mst.edges),
        "bst_height": bst.height(),
    }


def main() -> None:
    output = ensure_output_dir()

    scenario_results = [
        run_scenario("rs", source=4314902, risk_min=0.80, output_dir=output),
        run_scenario("matopiba", source=2105302, risk_min=0.75, output_dir=output),
    ]

    records = run_benchmark()
    data_dir = Path("data/processed")
    data_dir.mkdir(parents=True, exist_ok=True)
    with (data_dir / "performance_records.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["algorithm", "n", "time_ms", "memory_mb", "operations", "cost"])
        for record in records:
            writer.writerow(
                [
                    record.algorithm,
                    record.n,
                    f"{record.time_ms:.6f}",
                    f"{record.memory_mb:.6f}",
                    record.operations,
                    f"{record.cost:.6f}",
                ]
            )

    with (data_dir / "scenario_summary.csv").open("w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "scenario",
            "source",
            "target",
            "high_risk",
            "brute_path",
            "brute_cost",
            "brute_calls",
            "greedy_path",
            "greedy_cost",
            "greedy_operations",
            "mst_cost",
            "mst_edges",
            "bst_height",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for result in scenario_results:
            row = result.copy()
            row["high_risk"] = "; ".join(result["high_risk"])
            writer.writerow(row)

    plot_performance(records, output / "desempenho_tempo.png")
    plot_optimality_gap(records, output / "gap_otimalidade.png")

    for result in scenario_results:
        print(f"Cenario: {result['scenario']}")
        print(f"Municipios de alto risco: {result['high_risk']}")
        print(
            "Forca Bruta:",
            result["brute_path"],
            f"custo={result['brute_cost']:.2f}",
            f"chamadas={result['brute_calls']}",
        )
        print(
            "Dijkstra:",
            result["greedy_path"],
            f"custo={result['greedy_cost']:.2f}",
            f"arestas_relaxadas={result['greedy_operations']}",
        )
        print(
            f"MST Prim: custo_total={result['mst_cost']:.2f}, "
            f"arestas={result['mst_edges']}, altura_bst={result['bst_height']}"
        )
        print()

    print(f"Figuras salvas em: {output}")
    print("Resultados tabulares salvos em: data/processed/performance_records.csv")
    print("Resumo dos cenarios salvo em: data/processed/scenario_summary.csv")


if __name__ == "__main__":
    main()
