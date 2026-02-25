#!/usr/bin/env python3
"""
Simple Ontology Data Viewer
Displays all classes, properties, and instances in a readable format
"""

import requests
import json
from typing import Dict, Any

API_URL = "http://localhost:5002/api/ontology"

def print_header(title: str):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def get_data(endpoint: str) -> Dict[str, Any]:
    """Fetch data from API endpoint"""
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error fetching {endpoint}: HTTP {response.status_code}")
            return {}
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {}

def show_statistics():
    """Display ontology statistics"""
    print_header("📊 Ontology Statistics")
    
    data = get_data("statistics")
    if data.get('success'):
        stats = data['data']
        print(f"Total Classes:          {stats.get('total_classes', 0)}")
        print(f"Total Properties:       {stats.get('total_properties', 0)}")
        print(f"  - Object Properties:  {stats.get('total_object_properties', 0)}")
        print(f"  - Data Properties:    {stats.get('total_data_properties', 0)}")
        print(f"Total Instances:        {stats.get('total_instances', 0)}")
        print(f"Max Hierarchy Depth:    {stats.get('max_hierarchy_depth', 0)}")

def show_classes():
    """Display all classes"""
    print_header("📚 Classes")
    
    data = get_data("classes")
    if data.get('success'):
        classes = data['data']
        print(f"Found {len(classes)} classes:\n")
        
        # Group by hierarchy level
        root_classes = [c for c in classes if not c.get('parent_classes') or c['parent_classes'] == []]
        child_classes = [c for c in classes if c.get('parent_classes') and c['parent_classes'] != []]
        
        # Show root classes
        for cls in root_classes:
            print(f"📦 {cls['label']} ({cls['id']})")
            if cls.get('description'):
                print(f"   Description: {cls['description']}")
            
            # Show children
            children = [c for c in child_classes if cls['id'] in c.get('parent_classes', [])]
            for child in children:
                print(f"   └─ {child['label']} ({child['id']})")
                if child.get('description'):
                    print(f"      Description: {child['description']}")
                
                # Show grandchildren
                grandchildren = [c for c in child_classes if child['id'] in c.get('parent_classes', [])]
                for gc in grandchildren:
                    print(f"      └─ {gc['label']} ({gc['id']})")
            print()

def show_properties():
    """Display all properties"""
    print_header("🔗 Properties")
    
    data = get_data("properties")
    if data.get('success'):
        properties = data['data']
        if not properties:
            print("No properties defined yet.\n")
            return
            
        print(f"Found {len(properties)} properties:\n")
        
        for prop in properties:
            prop_type = prop.get('property_type', 'UNKNOWN')
            icon = "🔗" if prop_type == "OBJECT" else "📝"
            print(f"{icon} {prop['label']} ({prop['id']})")
            print(f"   Type: {prop_type}")
            if prop.get('description'):
                print(f"   Description: {prop['description']}")
            if prop.get('domain'):
                print(f"   Domain: {', '.join(prop['domain'])}")
            if prop.get('range'):
                print(f"   Range: {', '.join(prop['range'])}")
            print()

def show_instances():
    """Display all instances"""
    print_header("📦 Instances")
    
    # Try to get instances - may not have this endpoint
    response = requests.get(f"{API_URL}/instances")
    
    if response.status_code == 404:
        print("Instances endpoint not available.\n")
        print("Listing instances by class instead:\n")
        
        # Get all classes and check for instances
        classes_data = get_data("classes")
        if classes_data.get('success'):
            for cls in classes_data['data']:
                # This is a workaround - would need proper endpoint
                print(f"  {cls['label']} instances: (need proper endpoint)")
        return
    
    data = response.json()
    if data.get('success'):
        instances = data['data']
        if not instances:
            print("No instances created yet.\n")
            return
            
        print(f"Found {len(instances)} instances:\n")
        
        # Group by class
        by_class = {}
        for inst in instances:
            class_id = inst.get('class_id', 'Unknown')
            if class_id not in by_class:
                by_class[class_id] = []
            by_class[class_id].append(inst)
        
        for class_id, instances in by_class.items():
            print(f"🏷️  {class_id} ({len(instances)} instances):")
            for inst in instances:
                print(f"   • {inst['label']} ({inst['id']})")
                if inst.get('properties'):
                    for key, val in inst['properties'].items():
                        print(f"     - {key}: {val}")
            print()

def show_hierarchy():
    """Display class hierarchy tree"""
    print_header("🌳 Class Hierarchy")
    
    data = get_data("hierarchy")
    if data.get('success'):
        hierarchy = data['data']
        print_tree(hierarchy, indent=0)

def print_tree(node: Dict[str, Any], indent: int = 0):
    """Recursively print hierarchy tree"""
    prefix = "  " * indent
    if indent == 0:
        print(f"📦 {node['label']} ({node['class_id']})")
    else:
        print(f"{prefix}└─ {node['label']} ({node['class_id']})")
    
    if node.get('instance_count', 0) > 0:
        print(f"{prefix}   [instances: {node['instance_count']}]")
    
    children = node.get('children', [])
    for child in children:
        print_tree(child, indent + 1)

def main():
    print("\n" + "="*70)
    print("  🧠 WALLY-CLEAN Ontology Editor - Data Viewer")
    print("="*70)
    
    # Check if API is accessible
    try:
        response = requests.get(f"{API_URL}/statistics")
        if response.status_code != 200:
            print("\n❌ Cannot connect to Ontology API")
            print("   Start it with: ./start_ontology.sh")
            print("   Or: source .venv/bin/activate && python3 ontology_api.py")
            return
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to Ontology API at http://localhost:5002")
        print("   Start it with: ./start_ontology.sh")
        return
    
    # Show all data
    show_statistics()
    show_classes()
    show_properties()
    show_instances()
    show_hierarchy()
    
    print("\n" + "="*70)
    print("  💡 To modify data, use the REST API:")
    print(f"     curl -X POST {API_URL}/classes -d '{{...}}'")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
