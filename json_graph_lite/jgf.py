from .common import inplace_del
from .common import inplace_update
from .common import obj_to_dict
from .common import only_keys
from .node import Node
from .edge import Edge
from .graph import Graph as BaseGraph
from .graphs import GraphList as BaseGraphList


class Graph(BaseGraph):
    NodeClass = Node
    EdgeClass = Edge
    _SCALAR_SLOTS = (BaseGraph.DIRECTED, BaseGraph.TYPE, BaseGraph.LABEL, BaseGraph.METADATA)

    @classmethod
    def from_dict(cls, dict_value):
        d = dict_value[cls.GRAPH]
        kwargs = only_keys(d, cls._SCALAR_SLOTS)
        kwargs[BaseGraph.DIRECTED] = d.get(BaseGraph.DIRECTED)
        return cls(
            nodes=[cls.NodeClass.from_dict(inplace_update(node, id=id)) for id, node in d.get(cls.NODES, {}).items()],
            edges=[cls.EdgeClass.from_dict(edge) for edge in d.get(cls.EDGES, [])],
            **kwargs
        )

    def to_dict(self):
        graph = obj_to_dict(self, self._SCALAR_SLOTS)
        if len(self._nodes) > 0:
            graph[self.NODES] = {node.id: inplace_del(node.to_dict(), "id") for node in self.nodes}
        if len(self._edges) > 0:
            graph[self.EDGES] = [edge.to_dict() for edge in self.edges]
        return {self.GRAPH: graph}


class Graphs(BaseGraphList):
    GraphClass = Graph
    _SCALAR_SLOTS = ()
