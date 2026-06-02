# Global Solution 2026 - Dynamic Programming

Projeto em Python para monitoramento de riscos ambientais com grafo ponderado,
BST, Forca Bruta, algoritmo Guloso e analise de desempenho.

## Integrantes

Preencha antes da entrega:

| RM | Nome |
| 571922 | Guilherme Damasio Roselli |
| 571090 | Antonio Lino da Silva JR | 
| 570948 | Lucas Mirando Leite |

## Cenarios brasileiros

O projeto instancia dois cenarios com dados sinteticos justificados:

- Rede de resposta a enchentes no Rio Grande do Sul: vertices sao municipios da
  regiao metropolitana de Porto Alegre e arestas representam tempo aproximado de
  deslocamento.
- Triagem de risco de seca no MATOPIBA: vertices sao municipios relevantes da
  regiao e o indice de risco representa uma combinacao sintetica de criticidade
  por NDVI e precipitacao.

Os dados sao sinteticos para manter a execucao reprodutivel sem depender de
download externo. As fontes reais recomendadas para substituicao futura sao
Defesa Civil RS, DNIT, INMET, MODIS/NASA e IBGE.

## Estrutura

```text
data/raw/                         dados brutos
data/processed/                   resultados gerados
src/data_structures.py            grafo, BST, listas, tuplas, dict, deque
src/brute_force.py                busca exaustiva com backtracking
src/greedy.py                     Dijkstra e Prim com heapq
src/performance_monitor.py        tempo, memoria e operacoes
src/visualizations.py             figuras obrigatorias
tests/test_algorithms.py          testes automatizados
main.py                           execucao principal
report/figures/                   figuras geradas
```

## Como rodar o projeto

Abra o PowerShell dentro da pasta do projeto ou execute:

```powershell
cd "caminho\para\Global_Solution_Dynamic_Programming"
```

Instale as dependencias:

```powershell
python -m pip install -r requirements.txt
```

Rode o projeto principal:

```powershell
python main.py
```

Rode os testes automatizados:

```powershell
python -m pytest -q
```

Se aparecer `4 passed`, os testes passaram corretamente.

## Onde ver os resultados

Depois de executar `python main.py`, os arquivos gerados ficam em:

```text
report/figures/                         graficos e visualizacoes
data/processed/performance_records.csv  tabela de desempenho
data/processed/scenario_summary.csv     resumo dos cenarios
report/relatorio_final.pdf              relatorio final em PDF
```

Para abrir pelo PowerShell:

```powershell
explorer .\report\figures
explorer .\report\relatorio_final.pdf
notepad .\data\processed\scenario_summary.csv
```

## O que o programa faz

```bash
python -m pip install -r requirements.txt
python main.py
pytest
```

Ao executar `python main.py`, o sistema:

- constroi o grafo de municipios;
- constroi a BST por indice de risco;
- consulta municipios com risco entre `0.80` e `1.00`;
- compara Forca Bruta e Dijkstra para rotas de atendimento nos cenarios RS e MATOPIBA;
- gera a MST com Prim nos dois cenarios;
- mede desempenho para `N = 5, 8, 10, 12, 20, 50, 100`;
- salva figuras em `report/figures/`;
- salva tabela em `data/processed/performance_records.csv`.
- salva resumo dos cenarios em `data/processed/scenario_summary.csv`.

## Estruturas de dados usadas

| Estrutura | Uso no projeto | Justificativa |
|---|---|---|
| `list` | listas de adjacencia, caminhos e resultados | iteracao simples e baixo overhead |
| `tuple` | municipio e arestas | dados imutaveis e leves |
| `dict` | grafo, distancias e predecessores | busca media `O(1)` por id |
| `set` | visitados no backtracking e Dijkstra | evita ciclos com pertencimento medio `O(1)` |
| `deque` | BFS auxiliar | remocao no inicio em `O(1)` |
| `heapq` | fronteira do Dijkstra e Prim | extracao do menor custo em `O(log V)` |
| BST | ordenacao por indice de risco | busca por intervalo e priorizacao |

## Complexidade

- Forca Bruta: enumera caminhos simples. No pior caso, cresce de forma
  fatorial/exponencial, tornando-se inviavel em grafos maiores.
- Dijkstra com heap: `O((V + E) log V)`, adequado para instancias reais.
- Prim com heap: `O(E log V)`, usado para gerar a arvore de cobertura minima.
- BST nao balanceada: insercao, busca e remocao custam `O(h)`, onde `h` e a
  altura da arvore; no pior caso `O(n)`.

## Escala de decisao

| Nivel | Recomendacao | Criterio |
|---|---|---|
| 1 | Forca Bruta somente para validacao | otima, mas inviavel para N grande |
| 2 | Dijkstra em grafo pequeno | mesmo custo da Forca Bruta e tempo menor |
| 3 | Dijkstra em grafo medio/grande | escalavel para resposta operacional |
| 4 | Prim para cobertura regional | adequado quando o objetivo e conectar todos os municipios com custo minimo |

## Figuras obrigatorias

As figuras sao geradas automaticamente:

- `report/figures/grafo_mst_rs.png`
- `report/figures/grafo_mst_matopiba.png`
- `report/figures/bst_risco_rs.png`
- `report/figures/bst_risco_matopiba.png`
- `report/figures/desempenho_tempo.png`
- `report/figures/gap_otimalidade.png`

O arquivo `report/relatorio_base.md` ja inclui titulo, legenda, fonte e
interpretacao textual das figuras. O PDF `report/relatorio_final.pdf` e um
rascunho gerado automaticamente para facilitar a entrega.
