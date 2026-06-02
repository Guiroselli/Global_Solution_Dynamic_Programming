# Relatorio Tecnico - Global Solution 2026

## 1. Identificacao e contexto

RA - NOME: preencher antes da entrega.

O projeto desenvolve um sistema de monitoramento e triagem de riscos ambientais
em municipios brasileiros. Foram escolhidos dois cenarios: resposta a enchentes
no Rio Grande do Sul e triagem de risco de seca no MATOPIBA. A escolha se
justifica pela relevancia social dos eventos extremos e pela existencia de
fontes publicas que poderiam alimentar uma versao real do sistema: Defesa Civil
RS, DNIT, INMET, MODIS/NASA e IBGE.

Os dados usados nesta implementacao sao sinteticos, mas coerentes com os
cenarios propostos. Essa decisao permite reproducao local, testes automatizados
e comparacao controlada entre os algoritmos sem depender de downloads externos.

## 2. Modelagem

O grafo `G = (V, E)` representa municipios como vertices e rotas como arestas
ponderadas. Cada vertice e uma tupla `(id, nome, indice_risco,
custo_atendimento, populacao)`. Cada aresta `(u, v, peso)` representa o tempo
aproximado de deslocamento entre dois municipios.

O grafo foi implementado como dicionario de listas de adjacencia:
`{id_municipio: [(vizinho, peso), ...]}`. Essa representacao foi escolhida
porque as redes dos cenarios sao esparsas. Uma matriz de adjacencia exigiria
`O(V^2)` espaco mesmo quando ha poucas rotas; a lista de adjacencia usa
`O(V + E)` e torna natural percorrer apenas os vizinhos existentes.

A BST organiza os municipios pelo indice de risco. Ela foi implementada do zero
com as classes `Node` e `BinarySearchTree`, contendo insercao, busca por
intervalo, percurso in-order, calculo de altura e remocao por id. O in-order
gera a priorizacao crescente de risco, enquanto a busca por intervalo retorna
rapidamente os municipios mais criticos.

### Tabela de estruturas de dados

| Estrutura | Onde foi usada | Justificativa de complexidade |
|---|---|---|
| Lista | adjacencia do grafo, caminhos, resultados | iteracao simples e armazenamento compacto |
| Tupla | vertices e arestas | imutabilidade para dados principais |
| Dicionario | grafo, custos acumulados, predecessores | acesso medio `O(1)` por id |
| Conjunto | visitados no backtracking e no Dijkstra | pertencimento medio `O(1)` e prevencao de ciclos |
| `deque` | BFS auxiliar | remocao do inicio em `O(1)` |
| `heapq` | fronteira do Dijkstra e do Prim | extracao do menor custo em `O(log V)` |
| BST | priorizacao por indice de risco | operacoes `O(h)`, onde `h` e a altura |

## 3. Complexidade

A Forca Bruta enumera todos os caminhos simples entre origem e destino usando
recursao e backtracking. Ela serve como oraculo de validacao em instancias
pequenas, mas o numero de possibilidades cresce de forma exponencial/fatorial.
Por isso, os testes empiricos limitam a Forca Bruta a `N <= 12`.

O algoritmo Guloso escolhido foi o Dijkstra com heap. Como todos os pesos sao
nao negativos, a escolha local do menor custo acumulado ainda nao fechado e
correta: quando um vertice e removido do heap com a menor distancia conhecida,
nenhum caminho futuro por pesos positivos consegue reduzi-la. A complexidade e
`O((V + E) log V)`.

O Prim tambem foi implementado para gerar a arvore geradora minima de cobertura.
Ele seleciona a menor aresta que conecta a arvore atual a um novo vertice e tem
complexidade `O(E log V)` com heap.

## 4. Resultados e figuras obrigatorias

**Figura 1 - Grafo de municipios com MST destacada.**  
Arquivo: `report/figures/grafo_mst_rs.png` e
`report/figures/grafo_mst_matopiba.png`.  
Fonte: dados sinteticos inspirados em Defesa Civil RS, DNIT, INMET, MODIS/NASA e
IBGE.  
Interpretacao: as arestas destacadas representam a cobertura minima obtida por
Prim. No RS, a MST conecta todos os municipios com custo total reduzido,
priorizando ligacoes curtas entre cidades proximas. Na pratica, essa estrutura
ajuda a planejar cobertura logistica inicial sem repetir rotas desnecessarias.

**Figura 2 - BST por indice de risco.**  
Arquivo: `report/figures/bst_risco_rs.png` e
`report/figures/bst_risco_matopiba.png`.  
Fonte: indices de risco sinteticos, inspirados em risco de enchente, NDVI e
precipitacao.  
Interpretacao: a arvore organiza os municipios por criticidade ambiental. A
busca por intervalo recupera rapidamente municipios acima de um limiar, como
`0.80` no RS e `0.75` no MATOPIBA. Isso permite separar uma fila de atendimento
de alto risco antes de calcular rotas.

**Figura 3 - Desempenho tempo x N.**  
Arquivo: `report/figures/desempenho_tempo.png`.  
Fonte: benchmark sintetico gerado por `src/performance_monitor.py`.  
Interpretacao: a Forca Bruta cresce rapidamente ate `N = 12`, enquanto Dijkstra
mantem tempos baixos ate `N = 100`. O cruzamento pratico ocorre quando o tempo e
o numero de chamadas recursivas da Forca Bruta deixam de ser aceitaveis para
uso interativo. Assim, a Forca Bruta e adequada para validacao, mas nao para
operacao real.

**Figura 4 - Gap de otimalidade.**  
Arquivo: `report/figures/gap_otimalidade.png`.  
Fonte: comparacao entre Forca Bruta e Dijkstra para instancias pequenas.  
Interpretacao: nos grafos testados, o gap fica em `0%`, pois Dijkstra encontra o
caminho minimo exato quando os pesos sao nao negativos. Isso valida a escolha
do guloso para o problema de menor caminho. Caso fosse usado um criterio guloso
mais simples, como escolher sempre a menor aresta local sem custo acumulado, o
gap poderia aparecer.

## 5. Escala de decisao

| Nivel | Alternativa | Qualidade | Custo computacional | Recomendacao |
|---|---|---|---|---|
| 1 | Forca Bruta | otimo global | muito alto | usar so como validacao |
| 2 | Dijkstra em N pequeno | otimo para pesos nao negativos | baixo | comparar com Forca Bruta |
| 3 | Dijkstra em N medio/grande | otimo para menor caminho | baixo/moderado | usar para rotas operacionais |
| 4 | Prim para cobertura | otimo para MST | baixo/moderado | usar para conectar todos os municipios |

A decisao final recomenda Dijkstra para priorizar atendimento a municipios de
alto risco a partir de um hub. Para planejamento de cobertura regional, Prim e
mais adequado porque minimiza o custo total de conexao da rede.

## 6. Conclusao

A solucao atende aos ODS 2, 9, 11 e 13 ao propor uma base computacional para
resposta ambiental, infraestrutura resiliente e adaptacao climatica. A BST
permite priorizar municipios por risco, o grafo modela a malha de deslocamento e
os algoritmos comparam otimalidade e escalabilidade. A recomendacao pratica e
usar Forca Bruta apenas como validacao em instancias pequenas e Dijkstra/Prim
para decisao operacional.

## 7. Referencias

- Cormen, T. et al. Introduction to Algorithms, 4th Ed.
- Sedgewick, R. e Wayne, K. Algorithms, 4th Ed.
- Skiena, S. The Algorithm Design Manual.
- Defesa Civil RS.
- DNIT.
- INMET.
- NASA Earthdata MODIS.
- IBGE.
