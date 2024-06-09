import os
from neomodel import config as neo_config, db

neo_config.DATABASE_URL = f"bolt://neo4j:password@udtneo4j"

# node_keys = ["JYhxXvPmVK", "OJLFn51F9B", "5vLGJqgGUb", "yellow"]

nodes = [
    {"node_key": "JYhxXvPmVK", "name": ""},
    {"node_key": "OJLFn51F9B", "name": ""},
    {"node_key": "5vLGJqgGUb", "name": ""},
    {"node_key": "yellow", "name": "yellow", "color": "yellow"},
    {
        "node_key": "green",
        "name": "green",
        "node_labels": ["Banana", "Orange"],
        "shape": "square",
    },
]


def create_color():
    return """
    n.color = CASE WHEN item.color IS NOT NULL THEN item.color
                  ELSE NULL END"""


query = f"""UNWIND $batch AS item
         MERGE (n:NetworkNode {{node_key: item.node_key}})
         ON CREATE SET
         FOREACH (ignoreMe IN CASE WHEN 'Banana' IN item.node_labels THEN [1] ELSE [] END | SET n:Banana)
         FOREACH (ignoreMe IN CASE WHEN 'Orange' IN item.node_labels THEN [1] ELSE [] END | SET n:Orange)
         n.name = item.name,
         {create_color()},
         n.createdAt = timestamp()
         RETURN n
"""

result = db.cypher_query(query, {"batch": nodes})

print(result)


# https://emacs.stackexchange.com/questions/57505/how-to-fix-docker-command-prompt

# PS1="\u@\h:\w\$ "


# query = """
#         UNWIND $batch AS item
#         MERGE (n:NetworkNode {node_key: item.node_key})
#         ON CREATE
#           SET n :Banana
#         SET n += item
#         RETURN n
#         """

# UNWIND $batch AS item
# MERGE (n:NetworkNode {node_key: item.node_key})
# ON CREATE
# SET CALL is apoc.when(true, 'RETURN 7 as b', 'RETURN 5 as b',{a:3})
# SET n += item
# RETURN n


# query = """UNWIND $batch AS item
# CALL apoc.merge.node(["NetworkNode"], {node_key: item.node_key}, {}) YIELD node AS n
# CALL apoc.when(
#     item.node_key = 'yellow',
#     'RETURN {name: "yellow1"} AS b',
#     'RETURN {name: item.name} AS b',
#     {item: item}
# ) YIELD value AS b
# ON CREATE
# SET n.name = b.name
# SET n += item
# RETURN n"""
