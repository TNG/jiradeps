# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import networkx as nx

from jiradeps import create_issue_digraph, remove_unconnected_nodes


def test_trivial_graph(epics, stories):
    graph = create_issue_digraph({epics[0].key: stories})
    assert graph.number_of_nodes() == 2
    assert graph.number_of_edges() == 1


def test_remove_unconnected_nodes(stories):
    graph = nx.DiGraph()
    graph.add_node(1)
    graph.add_node(2)
    graph.add_node(3, issue='test issue')
    graph.add_edge(1, 2)
    assert len(graph) == 3

    removed_issues = remove_unconnected_nodes(graph)

    assert len(graph) == 2
    assert removed_issues == {'test issue'}

