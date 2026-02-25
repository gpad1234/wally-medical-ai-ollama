#!/usr/bin/env python3
"""
Ontology Editor Demo

Demonstrates creating and managing a university domain ontology.
"""

import sys
import json
from src.services.ontology_service import OntologyService
from src.services.ontology_models import (
    OntologyClass,
    OntologyProperty,
    OntologyInstance,
    PropertyType,
    PropertyCharacteristic,
)


def print_section(title: str):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def demo_university_ontology():
    """Create a complete university ontology example"""
    
    print_section("🧠 Ontology Editor Demo - University Domain")
    
    # Initialize service
    onto = OntologyService()
    
    # ========================================================================
    # Step 1: Create Class Hierarchy
    # ========================================================================
    print_section("Step 1: Creating Class Hierarchy")
    
    classes = [
        OntologyClass(
            id="Person",
            label="Person",
            description="A human being",
            parent_classes=["owl:Thing"]
        ),
        OntologyClass(
            id="Organization",
            label="Organization",
            description="An organized group",
            parent_classes=["owl:Thing"]
        ),
        OntologyClass(
            id="Student",
            label="Student",
            description="A person enrolled in courses",
            parent_classes=["Person"]
        ),
        OntologyClass(
            id="Professor",
            label="Professor",
            description="A faculty member who teaches",
            parent_classes=["Person"]
        ),
        OntologyClass(
            id="Course",
            label="Course",
            description="An educational unit",
            parent_classes=["owl:Thing"]
        ),
        OntologyClass(
            id="Department",
            label="Department",
            description="Academic division",
            parent_classes=["Organization"]
        ),
        OntologyClass(
            id="UndergraduateStudent",
            label="Undergraduate Student",
            description="Student pursuing bachelor's degree",
            parent_classes=["Student"]
        ),
        OntologyClass(
            id="GraduateStudent",
            label="Graduate Student",
            description="Student in graduate program",
            parent_classes=["Student"]
        ),
    ]
    
    for cls in classes:
        onto.create_class(cls)
        print(f"✅ Created class: {cls.label}")
    
    # ========================================================================
    # Step 2: Create Properties
    # ========================================================================
    print_section("Step 2: Creating Properties")
    
    properties = [
        OntologyProperty(
            id="teaches",
            label="teaches",
            property_type=PropertyType.OBJECT,
            description="Professor teaches a course",
            domain=["Professor"],
            range=["Course"]
        ),
        OntologyProperty(
            id="enrolledIn",
            label="enrolled in",
            property_type=PropertyType.OBJECT,
            description="Student enrolled in a course",
            domain=["Student"],
            range=["Course"]
        ),
        OntologyProperty(
            id="worksFor",
            label="works for",
            property_type=PropertyType.OBJECT,
            description="Person works for organization",
            domain=["Person"],
            range=["Organization"]
        ),
        OntologyProperty(
            id="hasName",
            label="has name",
            property_type=PropertyType.DATA,
            description="Name of entity",
            domain=["owl:Thing"],
            range=["string"]
        ),
        OntologyProperty(
            id="hasEmail",
            label="has email",
            property_type=PropertyType.DATA,
            description="Email address",
            domain=["Person"],
            range=["string"],
            characteristics={PropertyCharacteristic.FUNCTIONAL}
        ),
        OntologyProperty(
            id="hasGPA",
            label="has GPA",
            property_type=PropertyType.DATA,
            description="Grade point average",
            domain=["Student"],
            range=["float"]
        ),
    ]
    
    for prop in properties:
        onto.create_property(prop)
        print(f"✅ Created property: {prop.label} ({prop.property_type.value})")
    
    # ========================================================================
    # Step 3: Create Instances
    # ========================================================================
    print_section("Step 3: Creating Instances")
    
    instances = [
        OntologyInstance(
            id="ComputerScience",
            label="Computer Science Department",
            class_ids=["Department"],
            properties={"hasName": "Computer Science"}
        ),
        OntologyInstance(
            id="Mathematics",
            label="Mathematics Department",
            class_ids=["Department"],
            properties={"hasName": "Mathematics"}
        ),
        OntologyInstance(
            id="DrSmith",
            label="Dr. Alice Smith",
            class_ids=["Professor"],
            properties={
                "hasName": "Alice Smith",
                "hasEmail": "alice.smith@university.edu"
            }
        ),
        OntologyInstance(
            id="DrJones",
            label="Dr. Bob Jones",
            class_ids=["Professor"],
            properties={
                "hasName": "Bob Jones",
                "hasEmail": "bob.jones@university.edu"
            }
        ),
        OntologyInstance(
            id="JohnDoe",
            label="John Doe",
            class_ids=["UndergraduateStudent"],
            properties={
                "hasName": "John Doe",
                "hasEmail": "john.doe@student.edu",
                "hasGPA": 3.7
            }
        ),
        OntologyInstance(
            id="JaneSmith",
            label="Jane Smith",
            class_ids=["GraduateStudent"],
            properties={
                "hasName": "Jane Smith",
                "hasEmail": "jane.smith@student.edu",
                "hasGPA": 3.9
            }
        ),
        OntologyInstance(
            id="CS101",
            label="Intro to Computer Science",
            class_ids=["Course"],
            properties={"hasName": "Introduction to Computer Science"}
        ),
        OntologyInstance(
            id="CS301",
            label="Data Structures",
            class_ids=["Course"],
            properties={"hasName": "Data Structures and Algorithms"}
        ),
    ]
    
    for inst in instances:
        onto.create_instance(inst)
        print(f"✅ Created instance: {inst.label}")
    
    # ========================================================================
    # Step 4: Display Class Hierarchy
    # ========================================================================
    print_section("Step 4: Class Hierarchy")
    
    hierarchy = onto.get_class_hierarchy()
    
    def print_hierarchy(node, indent=0):
        prefix = "  " * indent
        print(f"{prefix}├─ {node.label} ({node.class_id})")
        if node.instance_count > 0:
            print(f"{prefix}│  └─ {node.instance_count} instance(s)")
        for child in node.children:
            print_hierarchy(child, indent + 1)
    
    print_hierarchy(hierarchy)
    
    # ========================================================================
    # Step 5: Query Examples
    # ========================================================================
    print_section("Step 5: Queries and Analysis")
    
    # Get all students
    students = onto.get_instances_of_class("Student", direct_only=False)
    print(f"📊 Total students: {len(students)}")
    for student in students:
        print(f"   - {student.label} (GPA: {student.properties.get('hasGPA', 'N/A')})")
    
    print()
    
    # Get all professors
    professors = onto.get_instances_of_class("Professor")
    print(f"📊 Total professors: {len(professors)}")
    for prof in professors:
        print(f"   - {prof.label}")
    
    print()
    
    # Get subclasses of Person
    person_subclasses = onto.get_subclasses("Person", direct_only=False)
    print(f"📊 Subclasses of Person: {len(person_subclasses)}")
    for cls in person_subclasses:
        print(f"   - {cls.label}")
    
    # ========================================================================
    # Step 6: Statistics
    # ========================================================================
    print_section("Step 6: Ontology Statistics")
    
    stats = onto.get_statistics()
    print(f"Total Classes: {stats.total_classes}")
    print(f"Total Properties: {stats.total_properties}")
    print(f"  - Object Properties: {stats.total_object_properties}")
    print(f"  - Data Properties: {stats.total_data_properties}")
    print(f"Total Instances: {stats.total_instances}")
    print(f"Max Hierarchy Depth: {stats.max_hierarchy_depth}")
    
    # ========================================================================
    # Step 7: Validation
    # ========================================================================
    print_section("Step 7: Validation")
    
    validation = onto.validate_ontology()
    if validation.valid:
        print("✅ Ontology is valid!")
    else:
        print("❌ Ontology has errors:")
        for error in validation.errors:
            print(f"   - {error['message']}")
    
    if validation.warnings:
        print(f"\n⚠️  {len(validation.warnings)} warning(s):")
        for warning in validation.warnings:
            print(f"   - {warning['message']}")
    
    # ========================================================================
    # Step 8: Consistency Check
    # ========================================================================
    print_section("Step 8: Consistency Check")
    
    consistency = onto.check_consistency()
    if consistency.consistent:
        print(f"✅ Ontology is consistent! (checked in {consistency.reasoning_time:.3f}s)")
    else:
        print("❌ Inconsistencies found:")
        for error in consistency.errors:
            print(f"   - {error}")
    
    # ========================================================================
    # Summary
    # ========================================================================
    print_section("✨ Demo Complete!")
    
    print("Created a complete university ontology with:")
    print(f"  • {stats.total_classes} classes (Person, Student, Professor, Course, etc.)")
    print(f"  • {stats.total_properties} properties (teaches, enrolledIn, hasGPA, etc.)")
    print(f"  • {stats.total_instances} instances (professors, students, courses)")
    print(f"  • {stats.max_hierarchy_depth} levels of hierarchy")
    print()
    print("🚀 API Server running at: http://localhost:5002")
    print("📚 Next steps:")
    print("  1. Start API: ./start_ontology.sh")
    print("  2. Try API: curl http://localhost:5002/api/ontology/classes")
    print("  3. View stats: curl http://localhost:5002/api/ontology/statistics")
    print()


if __name__ == '__main__':
    try:
        demo_university_ontology()
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
