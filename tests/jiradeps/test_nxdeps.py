# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

from unittest.mock import MagicMock
from pytest import fixture

from jiradeps import create_issue_digraph


@fixture
def test_data():
    class test_story:
        id = 1
        key = 'TEST-123'
        fields = MagicMock()

    return {
        'TEST-123': [test_story()]
    }


def test_trivial_graph(test_data):
    graph = create_issue_digraph(test_data)
    assert graph.number_of_nodes() == 1
    assert graph.number_of_edges() == 0
