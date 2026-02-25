#!/usr/bin/env python3
"""
Import sample data into Ontology Editor
Loads ontology data from JSON files via the REST API
"""

import json
import sys
import requests
from pathlib import Path
from typing import Dict, Any

API_BASE_URL = "http://localhost:5002/api/ontology"

class OntologyImporter:
    def __init__(self, api_url: str = API_BASE_URL):
        self.api_url = api_url
        self.stats = {
            'classes': 0,
            'properties': 0,
            'instances': 0,
            'relationships': 0,
            'errors': []
        }
    
    def load_file(self, filepath: str) -> Dict[str, Any]:
        """Load JSON data file"""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def import_classes(self, classes: list):
        """Import ontology classes"""
        print(f"\n📚 Importing {len(classes)} classes...")
        for cls in classes:
            try:
                response = requests.post(
                    f"{self.api_url}/classes",
                    json=cls,
                    headers={'Content-Type': 'application/json'}
                )
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print(f"  ✅ {cls['label']}")
                        self.stats['classes'] += 1
                    else:
                        print(f"  ⚠️  {cls['label']}: {result.get('message', 'Unknown error')}")
                        self.stats['errors'].append(f"Class {cls['id']}: {result.get('message')}")
                else:
                    print(f"  ❌ {cls['label']}: HTTP {response.status_code}")
                    self.stats['errors'].append(f"Class {cls['id']}: HTTP {response.status_code}")
            except Exception as e:
                print(f"  ❌ {cls['label']}: {str(e)}")
                self.stats['errors'].append(f"Class {cls['id']}: {str(e)}")
    
    def import_properties(self, properties: list):
        """Import ontology properties"""
        print(f"\n🔗 Importing {len(properties)} properties...")
        for prop in properties:
            try:
                response = requests.post(
                    f"{self.api_url}/properties",
                    json=prop,
                    headers={'Content-Type': 'application/json'}
                )
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print(f"  ✅ {prop['label']}")
                        self.stats['properties'] += 1
                    else:
                        print(f"  ⚠️  {prop['label']}: {result.get('message', 'Unknown error')}")
                        self.stats['errors'].append(f"Property {prop['id']}: {result.get('message')}")
                else:
                    print(f"  ❌ {prop['label']}: HTTP {response.status_code}")
                    self.stats['errors'].append(f"Property {prop['id']}: HTTP {response.status_code}")
            except Exception as e:
                print(f"  ❌ {prop['label']}: {str(e)}")
                self.stats['errors'].append(f"Property {prop['id']}: {str(e)}")
    
    def import_instances(self, instances: list):
        """Import ontology instances"""
        print(f"\n📦 Importing {len(instances)} instances...")
        for inst in instances:
            try:
                response = requests.post(
                    f"{self.api_url}/instances",
                    json=inst,
                    headers={'Content-Type': 'application/json'}
                )
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print(f"  ✅ {inst['label']}")
                        self.stats['instances'] += 1
                    else:
                        print(f"  ⚠️  {inst['label']}: {result.get('message', 'Unknown error')}")
                        self.stats['errors'].append(f"Instance {inst['id']}: {result.get('message')}")
                else:
                    print(f"  ❌ {inst['label']}: HTTP {response.status_code}")
                    self.stats['errors'].append(f"Instance {inst['id']}: HTTP {response.status_code}")
            except Exception as e:
                print(f"  ❌ {inst['label']}: {str(e)}")
                self.stats['errors'].append(f"Instance {inst['id']}: {str(e)}")
    
    def import_relationships(self, relationships: list):
        """Import relationships between instances"""
        print(f"\n🔗 Importing {len(relationships)} relationships...")
        for rel in relationships:
            try:
                # This would need a specific endpoint for adding relationships
                # For now, we'll note it
                print(f"  ⚠️  {rel['from']} --[{rel['property']}]--> {rel['to']} (manual step needed)")
                self.stats['relationships'] += 1
            except Exception as e:
                print(f"  ❌ Relationship: {str(e)}")
                self.stats['errors'].append(f"Relationship {rel}: {str(e)}")
    
    def import_file(self, filepath: str):
        """Import complete ontology from file"""
        print(f"\n{'='*60}")
        print(f"📥 Importing ontology from: {filepath}")
        print(f"{'='*60}")
        
        try:
            data = self.load_file(filepath)
            
            print(f"\n📋 Ontology: {data.get('name', 'Unknown')}")
            print(f"📝 Description: {data.get('description', 'N/A')}")
            print(f"🔢 Version: {data.get('version', 'N/A')}")
            
            # Import in order: classes -> properties -> instances -> relationships
            if 'classes' in data:
                self.import_classes(data['classes'])
            
            if 'properties' in data:
                self.import_properties(data['properties'])
            
            if 'instances' in data:
                self.import_instances(data['instances'])
            
            if 'relationships' in data:
                self.import_relationships(data['relationships'])
            
            # Show summary
            print(f"\n{'='*60}")
            print(f"✨ Import Summary")
            print(f"{'='*60}")
            print(f"✅ Classes imported:       {self.stats['classes']}")
            print(f"✅ Properties imported:    {self.stats['properties']}")
            print(f"✅ Instances imported:     {self.stats['instances']}")
            print(f"⚠️  Relationships noted:   {self.stats['relationships']}")
            
            if self.stats['errors']:
                print(f"\n❌ Errors encountered:     {len(self.stats['errors'])}")
                for error in self.stats['errors'][:5]:  # Show first 5 errors
                    print(f"   - {error}")
                if len(self.stats['errors']) > 5:
                    print(f"   ... and {len(self.stats['errors']) - 5} more")
            else:
                print(f"\n🎉 No errors!")
            
            print(f"\n📊 View results:")
            print(f"   curl {self.api_url}/statistics")
            print(f"   curl {self.api_url}/classes")
            
        except FileNotFoundError:
            print(f"❌ Error: File not found: {filepath}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in file: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 import_ontology.py <json_file>")
        print("\nAvailable sample files:")
        print("  sample_data/university_ontology.json")
        print("  sample_data/biomedical_ontology.json")
        print("\nExample:")
        print("  python3 import_ontology.py sample_data/university_ontology.json")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/statistics")
        if response.status_code != 200:
            print("❌ Error: Ontology API is not responding")
            print("   Start it with: ./start_ontology.sh")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to Ontology API at http://localhost:5002")
        print("   Start it with: ./start_ontology.sh")
        sys.exit(1)
    
    print("✅ Connected to Ontology API")
    
    # Import the data
    importer = OntologyImporter()
    importer.import_file(filepath)

if __name__ == "__main__":
    main()
