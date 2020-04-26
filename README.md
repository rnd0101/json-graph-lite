Lightweight library for JSON graph 
==================================

A practical implementation for:

https://github.com/jsongraph/json-graph-specification

Multigraphs are not supported. Incompatible change: list is used for nodes, not object, because JSON object looses
integer keys.

Code here follows some conventions from:

https://github.com/jsongraph/jsongraph.py

However, nothing substantial has been borrowed from there.

The intention of json-graph-lite is to provide lightweight graph library, which serializes
and deserializes graphs a la JSON graph format.

**NB: This library uses list for nodes, not object, so it's not really compatible with JSON Graph Format,
but sports better support for non-string node ids.**
