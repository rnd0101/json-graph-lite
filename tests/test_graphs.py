import json
from copy import deepcopy

import pytest

from json_graph_lite.edge import Edge
from json_graph_lite.graph import Graph
from json_graph_lite.graphs import GraphList
from json_graph_lite.node import Node

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
    'nodes': [{'id': 'a', 'label': 'node A', 'metadata': {'w': 1.3}},
              {'id': 'b', 'label': 'node B', 'metadata': {'w': 0.3}}],
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
    'nodes': [{'id': 'a', 'label': 'node A', 'metadata': {'w': 0.3}},
              {'id': 'b', 'label': 'node B', 'metadata': {'w': 5.3}}],
    'type': 'graph type'
}

GRAPH_FIXTURE = {
    'graph': GRAPH1
}

GRAPH2_FIXTURE = {
    'graph': GRAPH1
}

GRAPHS_FIXTURE = {
    'metadata': {
        'comment': 'JGF does not allow metadata here'
    },
    'graphs': [
        GRAPH1,
        GRAPH2
    ]
}


def test_graph_round_trip():
    g = Graph(
        nodes=[Node(id="a"), Node(id="b")],
        edges=[Edge(source="a", target="b")])
    d = g.to_dict()
    assert d == {
        'graph': {
            'directed': True,
            'edges': [{'source': 'a', 'target': 'b'}],
            'nodes': [{'id': 'a'}, {'id': 'b'}]}}

    g1 = Graph.from_dict(d)
    assert g1.to_dict() == g.to_dict()


def test_graph_round_trip_int_ids():
    g = Graph(
        nodes=[Node(id=1), Node(id=2)],
        edges=[Edge(source=1, target=2)])
    d = g.to_dict()
    assert d == {
        'graph': {
            'directed': True,
            'edges': [{'source': 1, 'target': 2}],
            'nodes': [{'id': 1}, {'id': 2}]}}

    d_json = json.dumps(d)
    d1 = json.loads(d_json)
    g1 = Graph.from_dict(d1)
    assert g1.to_dict() == g.to_dict()

    d_json2 = str(g)
    g2 = Graph.from_json(d_json2)
    assert g2.to_dict() == g.to_dict()


def test_graph_with_metadata():
    node1 = Node(id="a", label="node A", metadata={"w": 1.3})
    node2 = Node(id="b", label="node B", metadata={"w": 0.3})
    edge = Edge(node1, node2, relation="edge AB", directed=True, metadata={"w": 3})
    g = Graph(
        nodes=[node1, node2],
        edges=[edge],
        directed=True,
        type="graph type",
        label="G",
        metadata={"tags": ["g"]}
    )
    d = g.to_dict()
    assert d == GRAPH_FIXTURE
    d_json = str(g)
    g1 = Graph.from_json(d_json)
    assert g1.to_dict() == g.to_dict()


def test_add_node_and_edge():
    g = Graph()
    g.add_node(Node(id="a", label="node A", metadata={"w": 1.3}))
    g.add_node(Node(id="b", label="node B", metadata={"w": 0.3}))
    g.add_edge(Edge("a", "b"))

    assert g.to_dict() == {
        'graph': {
            'directed': True,
            'edges': [{'directed': True, 'source': 'a', 'target': 'b'}],
            'nodes': [{'id': 'a', 'label': 'node A', 'metadata': {'w': 1.3}},
                      {'id': 'b', 'label': 'node B', 'metadata': {'w': 0.3}}]
        }
    }

    with pytest.raises(TypeError) as excinfo:
        g.add_node(Edge("a", "b"))
    assert 'Type Node expected' in repr(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        g.add_edge(Edge("a", "b", directed=False))
    assert 'Adding undirected edge to directed graph' in repr(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        g.add_edge(Edge("a", "nosuch"))
    assert 'No such nodes' in repr(excinfo.value)


def test_in_out_edges():
    g = Graph.from_dict(deepcopy(GRAPH_FIXTURE))
    assert [e.relation for e in g.out_edges('a')] == ['edge AB']
    assert [e.relation for e in g.in_edges('b')] == ['edge AB']
    g.directed = False
    assert [e.relation for e in g.out_edges('b')] == ['edge AB']
    assert [e.relation for e in g.in_edges('a')] == ['edge AB']


def test_find_nodes():
    g = Graph.from_dict(deepcopy(GRAPH_FIXTURE))
    assert g.get_nodes(lambda node: node.id == 'nosuch') == []
    found = g.get_nodes(lambda node: node.id == 'a')
    assert len(found) == 1
    assert found[0].id == 'a' and found[0].label == 'node A'

    found = g.get_nodes(lambda node: node.id in {'a', 'b'})
    assert len(found) == 2

    g.add_node(Node(id="c", label="node C", metadata={"w": -0.1}))
    found = g.get_nodes(lambda e: e)
    assert len(found) == 3

    found = g.get_nodes(lambda e: e.metadata and e.metadata.get("w", 0.0) > 0)
    assert len(found) == 2

    with pytest.raises(ValueError) as excinfo:
        g.get_nodes("1")
    assert 'Criteria is not callable.' in repr(excinfo.value)


def test_find_edges():
    g = Graph.from_dict(deepcopy(GRAPH_FIXTURE))
    g.add_node(Node(id="c", label="node C", metadata={"w": -0.1}))
    g.add_edge(Edge("a", "c"))
    assert g.get_edges(lambda e: e.source == 'b') == []

    found = g.get_edges(lambda e: e.source == 'a' and e.target == 'b')
    assert len(found) == 1

    found = g.get_edges(lambda e: e.source == 'a')
    assert len(found) == 2
    assert found[0].target != found[1].target


def test_graphs_round_trip():
    graph_list = GraphList.from_dict(GRAPHS_FIXTURE)
    assert graph_list.to_dict() == GRAPHS_FIXTURE


def test_graphs_json_round_trip():
    graph_list = GraphList.from_dict(GRAPHS_FIXTURE)
    gl_json = str(graph_list)
    graph_list1 = GraphList.from_json(gl_json)
    assert graph_list1.to_dict() == graph_list.to_dict()


def test_add_graphs():
    graph_list = GraphList()
    g1 = Graph.from_dict(GRAPH_FIXTURE)
    graph_list.append(g1)

    assert graph_list.to_dict() == {
        'graphs': [
            {
                'directed': True,
                'edges': [{'directed': True,
                           'metadata': {'w': 3},
                           'relation': 'edge AB',
                           'source': 'a',
                           'target': 'b'}],
                'label': 'G',
                'metadata': {'tags': ['g']},
                'nodes': [{'id': 'a',
                           'label': 'node A',
                           'metadata': {'w': 1.3}},
                          {'id': 'b',
                           'label': 'node B',
                           'metadata': {'w': 0.3}}],
                'type': 'graph type'
            }
        ]
    }

    graph_list.append(g1)

    g2 = Graph.from_dict(GRAPH_FIXTURE)
    g2.id = "2"
    graph_list.append(g2)

    assert graph_list.graphs == [g1, g1, g2]

    with pytest.raises(ValueError) as excinfo:
        graph_list.append(g2)
    assert 'Graph already exists' in repr(excinfo.value)


def test_graphs_setter():
    graph_list = GraphList()
    assert len(graph_list) == 0

    g1 = Graph.from_dict(GRAPH_FIXTURE)
    graph_list.graphs = [g1]
    assert len(graph_list) == 1


def test_empty_graphs():
    assert GraphList().to_dict() == {'graphs': []}


def test_get_graph():
    graph_list = GraphList()
    assert len(graph_list) == 0

    g1 = Graph.from_dict(GRAPH_FIXTURE)
    g1.id = "1"

    g2 = Graph.from_dict(GRAPH2_FIXTURE)
    g2.id = "2"

    graph_list.append(g1)
    assert len(graph_list) == 1
    graph_list.append(g2)
    assert len(graph_list) == 2

    assert graph_list.get_graphs(lambda g: g.id == 'nosuch') == []
    assert graph_list.get_graphs(lambda g: g.id == '1') == [g1]


if __name__ == "__main__":
    pytest.main([__file__])
