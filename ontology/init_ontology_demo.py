#!/usr/bin/env python3
"""
Initialize Ontology with Demo Data

Creates sample classes, properties, and instances for testing Phase 1 inheritance.
"""

import sys
from src.services.ontology_service import OntologyService
from src.services.ontology_models import (
    OntologyClass,
    OntologyProperty,
    OntologyInstance,
    PropertyType,
    XSDDatatype,
)

def main():
    """Initialize ontology with demo data"""
    print("🧬 Initializing Ontology Demo Data...")
    print("=" * 60)
    
    # Initialize service (creates database if needed)
    service = OntologyService()
    print("✓ Ontology service initialized")
    
    # Create Person class
    print("\n📝 Creating classes...")
    person_class = OntologyClass(
        id="demo:Person",
        label="Person",
        description="A human being",
        parent_classes=["owl:Thing"]
    )
    service.create_class(person_class)
    print("  ✓ Created Person class")
    
    # Create Professor class (extends Person)
    professor_class = OntologyClass(
        id="demo:Professor",
        label="Professor",
        description="A university professor",
        parent_classes=["demo:Person"]
    )
    service.create_class(professor_class)
    print("  ✓ Created Professor class (extends Person)")
    
    # Create Student class (extends Person)
    student_class = OntologyClass(
        id="demo:Student",
        label="Student",
        description="A university student",
        parent_classes=["demo:Person"]
    )
    service.create_class(student_class)
    print("  ✓ Created Student class (extends Person)")
    
    # Create Employee class (extends Person)
    employee_class = OntologyClass(
        id="demo:Employee",
        label="Employee",
        description="An employee of an organization",
        parent_classes=["demo:Person"]
    )
    service.create_class(employee_class)
    print("  ✓ Created Employee class (extends Person)")
    
    # Create properties for Person
    print("\n🔧 Creating properties...")
    
    # name property (required)
    name_prop = OntologyProperty(
        id="demo:name",
        label="name",
        description="Full name of the person",
        property_type=PropertyType.DATA,
        domain=["demo:Person"],
        range=[str(XSDDatatype.STRING)],
        annotations={"required": "true"}
    )
    service.create_property(name_prop)
    print("  ✓ Created 'name' property (required, domain: Person)")
    
    # email property (required)
    email_prop = OntologyProperty(
        id="demo:email",
        label="email",
        description="Email address",
        property_type=PropertyType.DATA,
        domain=["demo:Person"],
        range=[str(XSDDatatype.STRING)],
        annotations={"required": "true"}
    )
    service.create_property(email_prop)
    print("  ✓ Created 'email' property (required, domain: Person)")
    
    # age property (optional)
    age_prop = OntologyProperty(
        id="demo:age",
        label="age",
        description="Age in years",
        property_type=PropertyType.DATA,
        domain=["demo:Person"],
        range=[str(XSDDatatype.INTEGER)]
    )
    service.create_property(age_prop)
    print("  ✓ Created 'age' property (optional, domain: Person)")
    
    # department property for Professor
    dept_prop = OntologyProperty(
        id="demo:department",
        label="department",
        description="Academic department",
        property_type=PropertyType.DATA,
        domain=["demo:Professor"],
        range=[str(XSDDatatype.STRING)],
        annotations={"required": "true"}
    )
    service.create_property(dept_prop)
    print("  ✓ Created 'department' property (required, domain: Professor)")
    
    # student_id property for Student
    sid_prop = OntologyProperty(
        id="demo:student_id",
        label="student_id",
        description="Student ID number",
        property_type=PropertyType.DATA,
        domain=["demo:Student"],
        range=[str(XSDDatatype.STRING)],
        annotations={"required": "true"}
    )
    service.create_property(sid_prop)
    print("  ✓ Created 'student_id' property (required, domain: Student)")
    
    # gpa property for Student
    gpa_prop = OntologyProperty(
        id="demo:gpa",
        label="gpa",
        description="Grade Point Average",
        property_type=PropertyType.DATA,
        domain=["demo:Student"],
        range=[str(XSDDatatype.FLOAT)]
    )
    service.create_property(gpa_prop)
    print("  ✓ Created 'gpa' property (optional, domain: Student)")
    
    # employee_id property for Employee
    eid_prop = OntologyProperty(
        id="demo:employee_id",
        label="employee_id",
        description="Employee ID number",
        property_type=PropertyType.DATA,
        domain=["demo:Employee"],
        range=[str(XSDDatatype.STRING)],
        annotations={"required": "true"}
    )
    service.create_property(eid_prop)
    print("  ✓ Created 'employee_id' property (required, domain: Employee)")
    
    # Create sample instances
    print("\n👤 Creating sample instances...")
    
    # Professor instance
    prof_instance = OntologyInstance(
        id="demo:prof_smith",
        label="Professor Smith",
        class_ids=["demo:Professor"],
        properties={
            "demo:name": "Dr. John Smith",
            "demo:email": "john.smith@university.edu",
            "demo:age": 45,
            "demo:department": "Computer Science"
        },
        annotations={"description": "Computer Science Professor"}
    )
    service.create_instance(prof_instance)
    print("  ✓ Created Professor Smith instance")
    
    # Student instance
    student_instance = OntologyInstance(
        id="demo:student_jones",
        label="Student Jones",
        class_ids=["demo:Student"],
        properties={
            "demo:name": "Alice Jones",
            "demo:email": "alice.jones@university.edu",
            "demo:age": 20,
            "demo:student_id": "S12345",
            "demo:gpa": 3.8
        },
        annotations={"description": "Computer Science Student"}
    )
    service.create_instance(student_instance)
    print("  ✓ Created Student Jones instance")
    
    # Employee instance
    employee_instance = OntologyInstance(
        id="demo:emp_brown",
        label="Employee Brown",
        class_ids=["demo:Employee"],
        properties={
            "demo:name": "Bob Brown",
            "demo:email": "bob.brown@university.edu",
            "demo:employee_id": "E98765"
        },
        annotations={"description": "University Staff Member"}
    )
    service.create_instance(employee_instance)
    print("  ✓ Created Employee Brown instance")
    
    # Get and display statistics
    print("\n📊 Ontology Statistics:")
    print("=" * 60)
    stats = service.get_statistics()
    print(f"  Classes: {stats.total_classes}")
    print(f"  Properties: {stats.total_properties}")
    print(f"  Instances: {stats.total_instances}")
    
    # Get graph stats from service
    graph_stats = service.graph_service.get_stats()
    print(f"  Total nodes: {graph_stats.node_count}")
    print(f"  Total edges: {graph_stats.edge_count}")
    
    # Test inheritance
    print("\n🧪 Testing Inheritance:")
    print("=" * 60)
    prof_full = service.get_class_full("demo:Professor")
    print(f"\nProfessor class:")
    print(f"  Direct properties: {len(prof_full['direct_properties'])}")
    print(f"  Inherited properties: {len(prof_full['inherited_properties'])}")
    print(f"  Total properties: {len(prof_full['all_properties'])}")
    
    print("\n  Direct properties:")
    for prop in prof_full['direct_properties']:
        req = "*" if prop.get('is_required') else ""
        print(f"    - {prop['label']}{req}")
    
    print("\n  Inherited properties:")
    for prop in prof_full['inherited_properties']:
        req = "*" if prop.get('is_required') else ""
        source = prop.get('inheritance_path', [None])[-1]
        print(f"    - {prop['label']}{req} (from {source})")
    
    print("\n✅ Demo data initialized successfully!")
    print("\n🚀 Next steps:")
    print("  1. Start the API: python3 ontology_api.py")
    print("  2. View in browser: http://localhost:5173")
    print("  3. Click 'Ontology Editor' tab")
    print("  4. Explore the Person → Professor/Student/Employee hierarchy!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
