import json
from copy import deepcopy

import pytest

from json_graph_lite.jgf import Graph
from json_graph_lite.jgf import Graphs

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
    'nodes': {
        'a': {'label': 'node A', 'metadata': {'w': 1.3}},
        'b': {'label': 'node B', 'metadata': {'w': 0.3}}
    },
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
    'nodes': {
        'a': {'label': 'node A', 'metadata': {'w': 0.3}},
        'b': {'label': 'node B', 'metadata': {'w': 5.3}}
    },
    'type': 'graph type'
}

GRAPH_FIXTURE = {
    'graph': GRAPH1
}

GRAPH2_FIXTURE = {
    'graph': GRAPH1
}

GRAPHS_FIXTURE = {
    'graphs': [
        GRAPH1,
        GRAPH2
    ]
}


def test_graph_round_trip():
    g1 = Graph.from_dict(deepcopy(GRAPH_FIXTURE))
    assert g1.to_dict() == GRAPH_FIXTURE


def test_graphs_round_trip():
    g1 = Graphs.from_dict(deepcopy(GRAPHS_FIXTURE))
    assert g1.to_dict() == GRAPHS_FIXTURE


EMPTY_GRAPH_EXAMPLE_FROM_JGF_PAGE = """{
  "graph": {}
}"""


NODES_ONLY_GRAPH_EXAMPLE_FROM_JGF_PAGE = """{
  "graph": {
    "nodes": {
      "A": {},
      "B": {}
    }
  }
}"""


SIMPLE_GRAPH_EXAMPLE_FROM_JGF_PAGE = """{
  "graph": {
    "nodes": {
      "A": {},
      "B": {}
    },
    "edges": [
      {
        "source": "A",
        "target": "B"
      }
    ]
  }
}"""


GRAPH_EXAMPLE_FROM_JGF_PAGE = """{
  "graph": {
    "directed": false,
    "type": "graph type",
    "label": "graph label",
    "metadata": {
      "user-defined": "values"
    },
    "nodes": {
      "0": {
        "type": "node type",
        "label": "node label(0)",
        "metadata": {
          "user-defined": "values"
        }
      },
      "1": {
        "type": "node type",
        "label": "node label(1)",
        "metadata": {
          "user-defined": "values"
        }
      }
    },
    "edges": [
      {
        "source": "0",
        "relation": "edge relationship",
        "target": "1",
        "directed": false,
        "label": "edge label",
        "metadata": {
          "user-defined": "values"
        }
      }
    ]
  }
}"""


@pytest.mark.parametrize("json_graph", [
    EMPTY_GRAPH_EXAMPLE_FROM_JGF_PAGE,
    NODES_ONLY_GRAPH_EXAMPLE_FROM_JGF_PAGE,
    SIMPLE_GRAPH_EXAMPLE_FROM_JGF_PAGE,
    GRAPH_EXAMPLE_FROM_JGF_PAGE,
])
def test_graph_from_jgf_spec_example(json_graph):
    g1 = Graph.from_json(NODES_ONLY_GRAPH_EXAMPLE_FROM_JGF_PAGE)
    assert json.loads(str(g1)) == json.loads(NODES_ONLY_GRAPH_EXAMPLE_FROM_JGF_PAGE)


EMPTY_GRAPHS_EXAMPLE_FROM_JGF_PAGE = """{
  "graphs": []
}"""


GRAPHS_EXAMPLE_FROM_JGF_PAGE = """{
  "graphs": [
    {
      "directed": true,
      "type": "graph type",
      "label": "graph label",
      "metadata": {
        "user-defined": "values"
      },
      "nodes": {
        "0": {
          "type": "node type",
          "label": "node label(0)",
          "metadata": {
            "user-defined": "values"
          }
        },
        "1": {
          "type": "node type",
          "label": "node label(1)",
          "metadata": {
            "user-defined": "values"
          }
        }
      },
      "edges": [
        {
          "source": "0",
          "relation": "edge relationship",
          "target": "1",
          "directed": true,
          "label": "edge label",
          "metadata": {
            "user-defined": "values"
          }
        }
      ]
    },
    {
      "directed": true,
      "type": "graph type",
      "label": "graph label",
      "metadata": {
        "user-defined": "values"
      },
      "nodes": {
        "0": {
          "type": "node type",
          "label": "node label(0)",
          "metadata": {
            "user-defined": "values"
          }
        },
        "1": {
          "type": "node type",
          "label": "node label(1)",
          "metadata": {
            "user-defined": "values"
          }
        }
      },
      "edges": [
        {
          "source": "1",
          "relation": "edge relationship",
          "target": "0",
          "directed": true,
          "label": "edge label",
          "metadata": {
            "user-defined": "values"
          }
        }
      ]
    }
  ]
}"""

@pytest.mark.parametrize("json_graphs", [
    EMPTY_GRAPHS_EXAMPLE_FROM_JGF_PAGE,
    GRAPHS_EXAMPLE_FROM_JGF_PAGE,
])
def test_graphs_from_jgf_spec_example(json_graphs):
    g1 = Graphs.from_json(json_graphs)
    assert json.loads(str(g1)) == json.loads(json_graphs)
