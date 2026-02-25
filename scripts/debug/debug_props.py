#!/usr/bin/env python3
"""Quick debug script to check properties"""

from src.services.ontology_service import OntologyService

# Initialize
onto = OntologyService()

# Check all nodes
print("All nodes in graph:")
for node_id in onto.graph.get_all_nodes():
    node_data = onto._get_node_data(node_id)
    node_type = node_data.get('node_type', 'unknown')
    label = node_data.get('label', 'no label')
    print(f"  {node_id}: {node_type} - {label}")

print("\nProperties specifically:")
all_props = onto.get_all_properties()
print(f"Found {len(all_props)} properties")
for prop in all_props:
    print(f"  - {prop.id}: {prop.label}")
