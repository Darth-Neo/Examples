# -*- coding: utf-8 -*-
"""
Computes minimum spanning tree of a weighted graph.

"""
#    Copyright (C) 2009-2010 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    Loïc Séguin-C. <loicseguin@gmail.com>
#    All rights reserved.
#    BSD license.

__all__ = ['kruskal_mst',
           'minimum_spanning_edges',
           'minimum_spanning_tree',
           'prim_mst_edges', 'prim_mst']

import networkx as nx
from heapq import heappop, heappush

#kruskal_mst=minimum_spanning_tree

def prim_mst_edges(G, weight = 'weight', data = True):
    """Generate edges in a minimum spanning forest of an undirected
    weighted graph.

    A minimum spanning tree is a subgraph of the graph (a tree)
    with the minimum sum of edge weights.  A spanning forest is a
    union of the spanning trees for each connected component of the graph.

    Parameters
    ----------
    G : NetworkX Graph

    weight : string
       Edge data key to use for weight (default 'weight').

    data : bool, optional
       If True yield the edge data along with the edge.

    Returns
    -------
    edges : iterator
       A generator that produces edges in the minimum spanning tree.
       The edges are three-tuples (u,v,w) where w is the weight.

    examples
    --------
    >>> G=nx.cycle_graph(4)
    >>> G.add_edge(0,3,weight=2) # assign weight 2 to edge 0-3
    >>> mst=nx.prim_mst_edges(G,data=False) # a generator of MST edges
    >>> edgelist=list(mst) # make a list of the edges
    >>> print(sorted(edgelist))
    [(0, 1), (1, 2), (2, 3)]

    Notes
    -----
    Uses Prim's algorithm.

    If the graph edges do not have a weight attribute a default weight of 1
    will be used.
    """

    if G.is_directed():
        raise nx.NetworkXError(
            "Mimimum spanning tree not defined for directed graphs.")

    nodes = G.nodes()

    while nodes:
        u = nodes.pop(0)
        frontier = []
        visited = [u]
        for u, v in G.edges(u):
            heappush(frontier, (G[u][v].get(weight, 1), u, v))

        while frontier:
            W, u, v = heappop(frontier)
            if v in visited:
                continue
            visited.append(v)
            nodes.remove(v)
            for v, w  in G.edges(v):
                if not w in visited:
                    heappush(frontier, (G[v][w].get(weight, 1), v, w))
            if data:
                yield u, v, G[u][v]
            else:
                yield u, v


def prim_mst(G, weight = 'weight'):
    """Return a minimum spanning tree or forest of an undirected weighted graph.

    A minimum spanning tree is a subgraph of the graph (a tree) with
    the minimum sum of edge weights.

    If the graph is not connected a spanning forest is constructed.  A
    spanning forest is a union of the spanning trees for each
    connected component of the graph.

    Parameters
    ----------
    G : NetworkX Graph

    weight : string
       Edge data key to use for weight (default 'weight').

    Returns
    -------
    G : NetworkX Graph
       A minimum spanning tree or forest.

    examples
    --------
    >>> G=nx.cycle_graph(4)
    >>> G.add_edge(0,3,weight=2) # assign weight 2 to edge 0-3
    >>> T=nx.prim_mst(G)
    >>> print(sorted(T.edges(data=True)))
    [(0, 1, {}), (1, 2, {}), (2, 3, {})]

    Notes
    -----
    Uses Prim's algorithm.

    If the graph edges do not have a weight attribute a default weight of 1
    will be used.
    """

    T=nx.Graph(nx.prim_mst_edges(G,weight=weight,data=True))
    # Add isolated nodes
    if len(T)!=len(G):
        T.add_nodes_from([n for n,d in G.degree().items() if d==0])
    # Add node and graph attributes as shallow copy
    for n in T:
        T.node[n]=G.node[n].copy()
    T.graph=G.graph.copy()
    return T

if __name__ == "__main__":
    G=nx.Graph()
    edgelist = [(0,3,[('weight',5)]),
                (0,1,[('weight',7)]),
                (1,3,[('weight',9)]),
                (1,2,[('weight',8)]),
                (1,4,[('weight',7)]),
                (3,4,[('weight',15)]),
                (3,5,[('weight',6)]),
                (2,4,[('weight',5)]),
                (4,5,[('weight',8)]),
                (4,6,[('weight',9)]),
                (5,6,[('weight',11)])]


    G.add_edges_from(edgelist)

    print G.number_of_nodes()
    print G.number_of_edges()
    print G.number_of_selfloops()

    for x in G:
        print "X: %s" % x

    NG = prim_mst(G)

    print NG.number_of_nodes()
    print NG.number_of_edges()
    print NG.number_of_selfloops()

    for y in G:
        print "%s-Y: %s" % (type(y), y)