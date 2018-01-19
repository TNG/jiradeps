# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

from pytest import fixture

from jiradeps import create_issue_digraph


@fixture
def test_data(epics, stories):

    return {
        epics[0].key: stories
    }


def test_trivial_graph(test_data):
    graph = create_issue_digraph(test_data)
    assert graph.number_of_nodes() == 2
    assert graph.number_of_edges() == 1
