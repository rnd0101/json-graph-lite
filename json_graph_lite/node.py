from .common import obj_to_dict
from .common import only_keys


class Node(object):
    ID = "id"
    LABEL = "label"
    TYPE = "type"
    METADATA = "metadata"
    __slots__ = (ID, LABEL, TYPE, METADATA)

    def __init__(self, id, label=None, type=None, metadata=None):
        self.id = id
        self.label = label
        self.type = type
        self.metadata = metadata

    @classmethod
    def from_dict(cls, d):
        return cls(**only_keys(d, cls.__slots__))

    def to_dict(self):
        return obj_to_dict(self, self.__slots__)
