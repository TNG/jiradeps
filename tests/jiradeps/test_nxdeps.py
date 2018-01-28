# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

from jiradeps import create_issue_digraph


def test_trivial_graph(epics, stories):
    graph = create_issue_digraph({epics[0].key: stories})
    assert graph.number_of_nodes() == 2
    assert graph.number_of_edges() == 1
