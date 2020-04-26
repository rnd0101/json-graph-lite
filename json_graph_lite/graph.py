from .common import check_condition
from .common import check_type
from .common import obj_to_dict
from .common import only_keys
from .edge import Edge
from .node import Node
import json


class Graph(object):
    NodeClass = Node
    EdgeClass = Edge
    json_module = json

    GRAPH = "graph"
    NODES = "nodes"
    EDGES = "edges"
    TYPE = "type"
    LABEL = "label"
    DIRECTED = "directed"
    METADATA = "metadata"
    _SCALAR_SLOTS = (DIRECTED, TYPE, LABEL, METADATA)
    __slots__ = _SCALAR_SLOTS + ("_nodes", "_edges")

    def __init__(self, nodes=None, edges=None, type=None, label=None, directed=True, metadata=None):
        self.directed = directed
        self.nodes = nodes or []
        self.edges = edges or []
        self.type = type
        self.label = label
        self.metadata = metadata

    @classmethod
    def from_dict(cls, dict_value):
        d = dict_value["graph"]
        return cls(
            nodes=[cls.NodeClass.from_dict(node) for node in d.get("nodes", [])],
            edges=[cls.EdgeClass.from_dict(edge) for edge in d.get("edges", [])],
            **only_keys(d, cls._SCALAR_SLOTS)
        )

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        self._nodes = [check_type(item, self.NodeClass) for item in value if item is not None]

    def has_nodes(self, nodes):
        return set(nodes).issubset({n.id for n in self.nodes})

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, value):
        self._edges = [
            check_condition(check_type(item, Edge), lambda x: self.has_nodes(x.nodes_ids), "No such nodes")
            for item in value if item is not None]

    def add_node(self, node):
        check_type(node, self.NodeClass)
        check_condition(node, lambda x: not self.has_nodes({node.id}),
                        "{} already exists".format(self.NodeClass.__name__))
        self._nodes.append(node)

    def add_edge(self, edge, force_direction=False):
        check_type(edge, Edge)
        if self.directed:
            if edge.directed is None or (not edge.directed and force_direction):
                edge.directed = True
            if not edge.directed:
                raise ValueError("Adding undirected edge to directed graph")
        self._edges.append(edge)

    def out_edges(self, node_id):
        if self.directed:
            return [edge for edge in self.edges if edge.source == node_id]
        else:
            return [edge for edge in self.edges if edge.source == node_id or edge.target == node_id]

    def in_edges(self, node_id):
        if self.directed:
            return [edge for edge in self.edges if edge.target == node_id]
        else:
            return [edge for edge in self.edges if edge.source == node_id or edge.target == node_id]

    def get_nodes(self, criteria=None):
        if callable(criteria):
            return [node for node in self.nodes if criteria(node)]
        raise ValueError("Criteria is not callable.")

    def get_edges(self, criteria=None):
        if callable(criteria):
            return [edge for edge in self.edges if criteria(edge)]
        raise ValueError("Criteria is not callable.")

    def to_dict(self):
        graph = obj_to_dict(self, self._SCALAR_SLOTS)
        if len(self._nodes) > 0:
            graph[self.NODES] = [node.to_dict() for node in self.nodes]
        if len(self._edges) > 0:
            graph[self.EDGES] = [edge.to_dict() for edge in self.edges]
        return {Graph.GRAPH: graph}

    def __str__(self):
        return self.json_module.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str):
        d = cls.json_module.loads(json_str)
        return cls.from_dict(d)
