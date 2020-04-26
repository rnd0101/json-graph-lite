from .common import obj_to_dict
from .common import only_keys
from .node import Node


class Edge(object):
    NodeClass = Node
    SOURCE = "source"
    TARGET = "target"
    RELATION = "relation"
    DIRECTED = "directed"
    METADATA = "metadata"
    __slots__ = (SOURCE, TARGET, RELATION, DIRECTED, METADATA)

    def __init__(self, source, target, relation=None, directed=None, metadata=None):
        self.source = source.id if isinstance(source, self.NodeClass) else source
        self.target = target.id if isinstance(target, self.NodeClass) else target
        self.relation = relation
        self.directed = directed
        self.metadata = metadata

    @classmethod
    def from_dict(cls, d):
        return cls(**only_keys(d, cls.__slots__))

    @property
    def nodes_ids(self):
        return {self.source, self.target}

    def to_dict(self):
        return obj_to_dict(self, self.__slots__)
