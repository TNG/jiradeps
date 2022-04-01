# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory
"""
Convert a networkx dependency graph to a .dot format with graphviz.
"""
import html
from collections import defaultdict
from typing import Any

import graphviz as gv
import networkx as nx

from .jirawrapper import get_related_keys
from .jirawrapper import get_sprints
from .jirawrapper import get_story_points
from .jirawrapper import get_team


def visualize_with_graphviz(
    nx_graph: nx.DiGraph,
    epics,
    file_name=None,
    file_type="svg",
    group_epics=False,
    align_sprints=False,
    show_status=False,
):
    """Render the graph and return the file path."""
    epics_by_key = {epic.key: epic for epic in epics}
    all_sprints: set[str] = set()
    for _, data in nx_graph.nodes(data=True):
        all_sprints |= get_sprints(data["issue"])
    hue_delta = 1 / (len(all_sprints) or 1)
    sprint_positions = {sprint: i for i, sprint in enumerate(sorted(all_sprints))}
    epics_nodes = defaultdict(set)
    epic_sprint_nodes: dict[str, dict[Any, set]] = defaultdict(lambda: defaultdict(set))

    graph = gv.Digraph(name=file_name, format=file_type, engine="dot")
    for node, data in nx_graph.nodes(data=True):
        issue = data["issue"]

        epics_nodes[data["epic"]].add(node)

        issue_sprints = sorted(get_sprints(issue))
        if issue_sprints:
            first_sprint_position = sprint_positions[issue_sprints[0]]
            sprint_display_number = str(first_sprint_position + 1)
            hue = first_sprint_position * hue_delta
            color = f"{hue:1.3f} {1:1.3f} {0.8:1.3f}"
            epic_sprint_nodes[data["epic"]][first_sprint_position].add(node)
        else:
            sprint_display_number = "?"
            color = "black"
        label = _get_node_label(
            issue, issue_sprints, sprint_display_number, data["max_pred_dist"], show_status=show_status
        )
        graph.node(node, label=label, shape="box", color=color)

    for edge in nx_graph.edges():
        graph.edge(*edge)

    if group_epics:
        for epic_key, nodes in epics_nodes.items():
            sub_graph = gv.Digraph("cluster" + epic_key)
            for node in nodes:
                sub_graph.node(node)
            epic = epics_by_key[epic_key]
            sub_graph.body.append(f"label = {_get_epic_label(epic)}")
            if align_sprints:
                sub_graph.body += [
                    "\t{{rank=same;{}}}".format(" ".join(sprint_nodes))
                    for sprint_nodes in epic_sprint_nodes[epic_key].values()
                ]
            graph.subgraph(sub_graph)
    else:
        if epic_sprint_nodes.values():
            if align_sprints:
                sprints_nodes = next(iter(epic_sprint_nodes.values())).values()
                graph.body += ["\t{{rank=same;{}}}".format(" ".join(sprint_nodes)) for sprint_nodes in sprints_nodes]

    return graph.render()


def _get_node_label(issue, sprints, sprint_display_number, max_pred_dist, show_status=False):
    lines = []

    if sprints:
        lines.append(
            "<{issue_key} ({sprint_position}/{max_pred_dist})".format(
                issue_key=issue.key, max_pred_dist=max_pred_dist + 1, sprint_position=sprint_display_number
            )
        )
    else:
        lines.append(f"<{issue.key} ({max_pred_dist + 1})")

    lines.append(f'<FONT POINT-SIZE="10">{html.escape(issue.fields.summary)}')

    info_fields = []
    story_points = get_story_points(issue)
    if story_points is not None:
        info_fields.append(f"SP: {story_points:.0f}")
    if sprints:
        info_fields.append("Sprint: {}".format(", ".join(sprints)))
    if info_fields:
        lines.append(" &nbsp; ".join(info_fields))

    if show_status:
        status_fields = [f"Status: {issue.fields.status.name}"]
        team = get_team(issue)
        if team:
            status_fields.append(f"Team: {team}")
        lines.append(" &nbsp; ".join(status_fields))

    relates_to = get_related_keys(issue)
    if relates_to:
        lines.append('<FONT color="blue">relates to: {}</FONT>'.format(", ".join(relates_to)))
    lines[-1] += "</FONT>>"
    return "<BR />".join(lines)


def _get_epic_label(epic):
    lines = [f'<<FONT POINT-SIZE="10">{epic.key}', f"{html.escape(epic.fields.summary)}</FONT>>"]
    return "<BR />".join(lines)
