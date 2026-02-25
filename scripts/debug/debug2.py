#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/gp/claude-code/startup-one/WALLY-CLEAN')

from src.services.ontology_service import OntologyService

onto = OntologyService()

print("Checking owl:Thing...")
print(f"Exists: {onto.graph.node_exists('owl:Thing')}")

node_data = onto.graph.get_node("owl:Thing")
print(f"Node data: {node_data}")
print(f"Node type: {node_data.get('node_type') if node_data else 'None'}")
print(f"CLASS_TYPE constant: {onto.CLASS_TYPE}")
print(f"Match: {node_data.get('node_type') == onto.CLASS_TYPE if node_data else False}")
