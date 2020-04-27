Lightweight library for JSON graph 
==================================

Library, similar to:

https://github.com/jsongraph/json-graph-specification

**NB: `json-graph-lite` library uses list for nodes, not object, so it's not really compatible with JSON Graph Format,
but sports better support for non-string node ids.** Multigraphs are not yet supported. Incompatible change: list is
used for nodes, not object, because JSON object can't represent integer keys.

Code here follows some conventions from:

https://github.com/jsongraph/jsongraph.py

However, nothing substantial has been borrowed from there.

The intention of json-graph-lite is to provide lightweight graph library, which serializes
and deserializes graphs a la JSON graph format.
