import networkx as nx
from .UnionFind import *

def minimum_spanning_edges(G, weight='weight', data=True):
    if G.is_directed():
        raise nx.NetworkXError(
            "Mimimum spanning tree not defined for directed graphs.")

    subtrees = UnionFind()
    edges = sorted(G.edges(data=True), key=lambda t: t[2].get(weight, 1))
    for u, v, d in edges:
        if subtrees[u] != subtrees[v]:
            if data:
                yield (u, v, d)
            else:
                yield (u, v)
            subtrees.union(u, v)

def minimum_spanning_tree(G, weight='weight'):
	T = nx.Graph(minimum_spanning_edges(G, weight=weight, data=True))
    # Add isolated nodes
    if len(T) != len(G):
        T.add_nodes_from([n for n, d in G.degree().items() if d == 0])
    # Add node and graph attributes as shallow copy
    for n in T:
        T.node[n] = G.node[n].copy()
    T.graph = G.graph.copy()
    return T