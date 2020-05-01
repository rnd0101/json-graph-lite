import json
from copy import deepcopy

import pytest

from json_graph_lite.jgf import Edge
from json_graph_lite.jgf import Graph
from json_graph_lite.jgf import Graphs
from json_graph_lite.jgf import Node

GRAPH1 = {
    'directed': True,
    'edges': [{
        'directed': True,
        'metadata': {'w': 3},
        'relation': 'edge AB',
        'source': 'a',
        'target': 'b'}],
    'label': 'G',
    'metadata': {'tags': ['g']},
    'nodes': {
        'a': {'label': 'node A', 'metadata': {'w': 1.3}},
        'b': {'label': 'node B', 'metadata': {'w': 0.3}}
    },
    'type': 'graph type'
}

GRAPH2 = {
    'directed': True,
    'edges': [{
        'directed': True,
        'metadata': {'w': 1},
        'relation': 'edge AB',
        'source': 'a',
        'target': 'b'}],
    'label': 'G2',
    'metadata': {'tags': ['g2']},
    'nodes': {
        'a': {'label': 'node A', 'metadata': {'w': 0.3}},
        'b': {'label': 'node B', 'metadata': {'w': 5.3}}
    },
    'type': 'graph type'
}

GRAPH_FIXTURE = {
    'graph': GRAPH1
}

GRAPH2_FIXTURE = {
    'graph': GRAPH1
}

GRAPHS_FIXTURE = {
    'graphs': [
        GRAPH1,
        GRAPH2
    ]
}


def test_graph_round_trip():
    g1 = Graph.from_dict(GRAPH_FIXTURE)
    assert g1.to_dict() == GRAPH_FIXTURE


def test_graphs_round_trip():
    g1 = Graphs.from_dict(GRAPHS_FIXTURE)
    assert g1.to_dict() == GRAPHS_FIXTURE
