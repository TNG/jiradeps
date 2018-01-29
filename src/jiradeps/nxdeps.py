# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory
"""
Create a networkx directed graph of the story dependencies.
"""

import itertools
import sys
import logging

import networkx as nx

from .jirawrapper import get_blocked_keys

log = logging.getLogger(__name__)


def create_issue_digraph(epics_stories):
    """Return a graph representation of all issues.
    
    Blocking dependencies are modelled as graph edges. 
    """
    log.info('creating graph...')
    graph = nx.DiGraph()
    for epic, stories in epics_stories.items():
        for issue in stories:
            graph.add_node(issue.id, issue=issue, epic=epic)
    for issue in itertools.chain(*epics_stories.values()):
        for target_issue_id in get_blocked_keys(issue):
            if target_issue_id not in graph.node:
                log.warning(f'issue {issue.key} blocks unknown issue {target_issue_id}')
                continue
            graph.add_edge(issue.id, target_issue_id)
    if not nx.is_directed_acyclic_graph(graph):
        log.error('graph has at least one cycle: {}'.format(nx.find_cycle(graph)))
        sys.exit(1)
    return graph


def add_longest_ancestor_distance(graph: nx.DiGraph):
    """Add the longest ancestor distance to all nodes in the graph."""
    log.info('longest path length: {}'.format(max(nx.dag_longest_path_length(graph) + 1, 1)))
    for node in nx.topological_sort(graph):
        max_dist_predecessors = [
            graph.node[predecessor]['max_pred_dist'] + 1 for predecessor in graph.predecessors(node)
        ]
        graph.node[node]['max_pred_dist'] = max(max_dist_predecessors, default=0)


def remove_unconnected_nodes(graph: nx.DiGraph):
    """Remove unconnected nodes and return the corresponding issues."""
    removed_nodes = [node for node in graph.nodes() if graph.degree(node) == 0]
    if removed_nodes:
        graph.remove_nodes_from(removed_nodes)
    return [graph.node[node]['issue'] for node in removed_nodes]
