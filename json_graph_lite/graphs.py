import json

from .graph import Graph
from .common import check_condition
from .common import check_type
from .common import obj_to_dict
from .common import only_keys
from .common import search_by_criteria


class GraphList(object):
    GraphClass = Graph
    json_module = json

    GRAPHS = "graphs"
    LABEL = "label"
    METADATA = "metadata"
    _SCALAR_SLOTS = (LABEL, METADATA)
    __slots__ = _SCALAR_SLOTS + ("_graphs",)

    def __init__(self, graphs=None, label=None, metadata=None):
        self._graphs = graphs or []
        self.label = label
        self.metadata = metadata

    @classmethod
    def from_dict(cls, dict_value):
        return cls(
            graphs=[cls.GraphClass.from_dict({cls.GraphClass.GRAPH: graph})
                    for graph in dict_value.get(cls.GRAPHS, [])],
            **only_keys(dict_value, cls._SCALAR_SLOTS)
        )

    @property
    def graphs(self):
        return self._graphs

    @graphs.setter
    def graphs(self, value):
        self._graphs = [check_type(item, self.GraphClass) for item in value if item is not None]

    def has_graph(self, graph_id):
        if graph_id is None:
            return False
        return any(graph_id == g.id for g in iter(self.graphs))

    def append(self, graph):
        check_type(graph, self.GraphClass)
        check_condition(graph, lambda x: not self.has_graph(x.id),
                        "{} already exists".format(self.GraphClass.__name__))
        self._graphs.append(graph)

    def get_graphs(self, criteria):
        return search_by_criteria(self.graphs, criteria)

    def to_dict(self):
        graphs = obj_to_dict(self, self._SCALAR_SLOTS)
        graphs[self.GRAPHS] = [graph.to_dict()[graph.GRAPH] for graph in self.graphs]
        return graphs

    def __len__(self):
        return len(self._graphs)

    def __str__(self):
        return self.json_module.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str):
        d = cls.json_module.loads(json_str)
        return cls.from_dict(d)
