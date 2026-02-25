"""
Test Graph Export

Simple script to demonstrate exporting a graph to structured text formats.
"""

from graph_db import GraphDB

# Create a graph
print("Creating graph...")
graph = GraphDB(directed=True, weighted=False)

# Add nodes with data
graph.add_node("A", {"label": "Start", "type": "input"})
graph.add_node("B", {"label": "Process 1", "type": "compute"})
graph.add_node("C", {"label": "Process 2", "type": "compute"})
graph.add_node("D", {"label": "End", "type": "output"})

# Add edges
graph.add_edge("A", "B")
graph.add_edge("A", "C")
graph.add_edge("B", "D")
graph.add_edge("C", "D")

print(f"✓ Created graph with {len(graph.get_all_nodes())} nodes and {len(graph.get_all_edges())} edges")
print()

# Export to JSON file
print("Exporting to JSON...")
with open("my_graph.json", "w") as f:
    f.write(graph.export_to_json(pretty=True))
print("✓ Saved to my_graph.json")
print()

# Export to adjacency list file
print("Exporting to adjacency list...")
with open("my_graph.txt", "w") as f:
    f.write(graph.export_to_adjacency_list())
print("✓ Saved to my_graph.txt")
print()

# Display the exports
print("=" * 60)
print("JSON Export (my_graph.json):")
print("=" * 60)
with open("my_graph.json", "r") as f:
    print(f.read())

print()
print("=" * 60)
print("Adjacency List Export (my_graph.txt):")
print("=" * 60)
with open("my_graph.txt", "r") as f:
    print(f.read())

print()
print("✓ Export complete! Check my_graph.json and my_graph.txt")
