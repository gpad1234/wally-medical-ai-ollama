#!/usr/bin/env python3
"""Quick debug script"""

import sys
sys.path.insert(0, '/Users/gp/claude-code/startup-one/WALLY-CLEAN')

from src.services.ontology_service import OntologyService

onto = OntologyService()

# Check owl:Thing
node = onto.graph_service.get_node("owl:Thing")
print(f"Node ID: {node.id}")
print(f"Node Label: {node.label}")
print(f"Node Properties: {node.properties}")
print(f"Node Type: {node.properties.get('node_type')}")

# Check node data directly
node_data = onto.graph.get_node_data("owl:Thing")
print(f"\nDirect Node Data: {node_data}")
