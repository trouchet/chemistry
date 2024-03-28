import networkx as nx
import matplotlib.pyplot as plt

def plotar_grafo_networkx(dados):
    """
    Plota um gráfico de rede utilizando a biblioteca NetworkX.

    Args:
        dados (list): Lista de tuplas contendo as informações dos nós e arestas do grafo. Cada tupla deve estar no formato (origem, destino, probabilidade, quantidade).

    Returns:
        matplotlib.pyplot: O objeto matplotlib.pyplot contendo o gráfico plotado.
    """
    G = nx.DiGraph()

    for origem, destino, prob, qtd in dados:
        G.add_node(origem, size=qtd)
        G.add_node(destino, size=qtd)
        color = 'blue' if prob > 0 else 'red'
        G.add_edge(origem, destino, weight=abs(prob)*10, color=color)

    sizes = [G.nodes[node]['size']*100 for node in G.nodes]
    edges = G.edges()
    colors = [G[u][v]['color'] for u,v in edges]
    weights = [G[u][v]['weight'] for u,v in edges]

    pos = nx.spring_layout(G)
    nx.draw(
        G, pos, node_size=sizes, edge_color=colors, width=weights, with_labels=True
    )

    return plt

def plotar_grafo_plt(rules, items):
    """
    Plota um diagrama de rede das regras de associação utilizando a biblioteca NetworkX.

    Args:
        rules (list): Lista de tuplas contendo as regras de associação.
        items (list): Lista de itens.

    Returns:
        matplotlib.pyplot: O objeto matplotlib.pyplot contendo o diagrama plotado.
    """
    # Create a dictionary of the items
    item_dict = {items[i]: i for i in range(len(items))}

    # Create a dictionary of the items in the rules
    rule_items = [
        (item_dict[antecedent], item_dict[consequent]) 
        for antecedent, consequent in rules
    ]

    # Create a weighted graph
    G = nx.DiGraph()
    G.add_weighted_edges_from(rule_items)

    # Set the node positions
    pos = nx.spring_layout(G, k=10)

    # Draw the nodes
    nx.draw_networkx_nodes(G, pos, node_size=1000)

    # Draw the edges
    nx.draw_networkx_edges(G, pos, width=1)

    # Show the plot
    return plt
