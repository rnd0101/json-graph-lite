from copy import deepcopy

from json_graph_lite.edge import Edge
from json_graph_lite.graph import Graph
from json_graph_lite.node import Node
import json

GRAPH_FIXTURE = {
    'graph': {
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


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
