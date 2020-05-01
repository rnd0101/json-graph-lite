Lightweight library for JSON graph 
==================================

Library, similar to:

https://github.com/jsongraph/jsongraph.py

**NB: `json-graph-lite` library uses list for nodes, not object, so it's not compatible with JSON Graph Format.**

JSON Graph Format compatible classes (Graph, Graphs) can be found from `json_graph_lite.jgf`.

Incompatible change: list is used for nodes, not object, because JSON object can't represent integer keys.

The intention of json-graph-lite is to provide lightweight graph library, which serializes
and deserializes graphs a la JSON graph format.

Take a look at [tests/test_graphs.py](tests/test_graphs.py) for usage examples.
