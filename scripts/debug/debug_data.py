#!/usr/bin/env python3
"""Debug property retrieval issue"""

from src.services.ontology_service import OntologyService

# Initialize
onto = OntologyService()

print("=== DEBUG: Property Retrieval ===\n")

# Get all nodes
print("All nodes in graph:")
for node_id in onto.graph.get_all_nodes():
    node_data = onto._get_node_data(node_id)
    node_type = node_data.get('node_type', 'MISSING')
    label = node_data.get('label', 'no label')
    print(f"  {node_id}: type={node_type}, label={label}")

print(f"\nPROPERTY_TYPE constant: '{onto.PROPERTY_TYPE}'")

# Try to get all properties
print("\nCalling get_all_properties()...")
try:
    props = onto.get_all_properties()
    print(f"Found {len(props)} properties:")
    for prop in props:
        print(f"  - {prop.id}: {prop.label}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

# Check edges for hierarchy
print("\nAll edges (showing first 20):")
edges = onto.graph.get_all_edges()
for i, (from_node, to_node, weight) in enumerate(edges[:20]):
    edge_data = onto.graph.get_edge(from_node, to_node)
    label = edge_data.get('label', 'no label') if edge_data else 'no data'
    print(f"  {from_node} --[{label}]--> {to_node}")
