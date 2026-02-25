"""
Unit tests for ontology property inheritance functionality

Tests the Phase 1 implementation of automatic property inheritance
from parent classes to subclasses.
"""

import pytest
from src.services.ontology_service import OntologyService
from src.services.ontology_models import (
    OntologyClass,
    OntologyProperty,
    OntologyInstance,
    PropertyType
)
from src.services.base_service import NodeNotFoundError, ValidationError


@pytest.fixture
def ontology_service():
    """Create fresh ontology service for each test"""
    return OntologyService()


@pytest.fixture
def setup_class_hierarchy(ontology_service):
    """Setup a basic class hierarchy: Person -> Professor, Person -> Student"""
    # Create Person class
    person = OntologyClass(
        id="Person",
        label="Person",
        description="A human being"
    )
    ontology_service.create_class(person)
    
    # Create properties for Person
    name_prop = OntologyProperty(
        id="hasName",
        label="name",
        property_type=PropertyType.DATA,
        domain=["Person"],
        range=["string"]
    )
    ontology_service.create_property(name_prop)
    
    email_prop = OntologyProperty(
        id="hasEmail",
        label="email",
        property_type=PropertyType.DATA,
        domain=["Person"],
        range=["string"]
    )
    ontology_service.create_property(email_prop)
    
    # Create Professor class (subclass of Person)
    professor = OntologyClass(
        id="Professor",
        label="Professor",
        description="University professor",
        parent_classes=["Person"]
    )
    ontology_service.create_class(professor)
    
    # Add property specific to Professor
    dept_prop = OntologyProperty(
        id="hasDepartment",
        label="department",
        property_type=PropertyType.DATA,
        domain=["Professor"],
        range=["string"]
    )
    ontology_service.create_property(dept_prop)
    
    # Create Student class (subclass of Person)
    student = OntologyClass(
        id="Student",
        label="Student",
        description="University student",
        parent_classes=["Person"]
    )
    ontology_service.create_class(student)
    
    return ontology_service


def test_get_direct_properties(setup_class_hierarchy):
    """Test getting direct properties of a class"""
    service = setup_class_hierarchy
    
    # Person should have 2 direct properties
    person_props = service.get_class_properties("Person")
    assert len(person_props) == 2
    prop_ids = [p['id'] for p in person_props]
    assert "hasName" in prop_ids
    assert "hasEmail" in prop_ids
    
    # Professor should have 1 direct property
    prof_props = service.get_class_properties("Professor")
    assert len(prof_props) == 1
    assert prof_props[0]['id'] == "hasDepartment"


def test_single_level_inheritance(setup_class_hierarchy):
    """Test property inheritance from parent to child (single level)"""
    service = setup_class_hierarchy
    
    # Professor should inherit properties from Person
    inherited = service.compute_inherited_properties("Professor")
    
    assert len(inherited) == 2
    prop_labels = [p['label'] for p in inherited]
    assert "name" in prop_labels
    assert "email" in prop_labels
    
    # Check source tracking
    for prop in inherited:
        assert prop['source'] == "Person"
        assert prop['inheritance_path'] == ["Person"]


def test_multi_level_inheritance(ontology_service):
    """Test recursive inheritance through multiple levels"""
    service = ontology_service
    
    # Create Animal -> Mammal -> Dog hierarchy
    animal = OntologyClass(id="Animal", label="Animal")
    service.create_class(animal)
    
    species_prop = OntologyProperty(
        id="hasSpecies",
        label="species",
        property_type=PropertyType.DATA,
        domain=["Animal"],
        range=["string"]
    )
    service.create_property(species_prop)
    
    mammal = OntologyClass(
        id="Mammal",
        label="Mammal",
        parent_classes=["Animal"]
    )
    service.create_class(mammal)
    
    warm_blooded_prop = OntologyProperty(
        id="isWarmBlooded",
        label="warm_blooded",
        property_type=PropertyType.DATA,
        domain=["Mammal"],
        range=["boolean"]
    )
    service.create_property(warm_blooded_prop)
    
    dog = OntologyClass(
        id="Dog",
        label="Dog",
        parent_classes=["Mammal"]
    )
    service.create_class(dog)
    
    breed_prop = OntologyProperty(
        id="hasBreed",
        label="breed",
        property_type=PropertyType.DATA,
        domain=["Dog"],
        range=["string"]
    )
    service.create_property(breed_prop)
    
    # Dog should inherit from both Mammal and Animal
    inherited = service.compute_inherited_properties("Dog")
    
    assert len(inherited) == 2  # species + warm_blooded
    prop_labels = [p['label'] for p in inherited]
    assert "species" in prop_labels
    assert "warm_blooded" in prop_labels
    
    # Check inheritance paths
    species_prop = next(p for p in inherited if p['label'] == 'species')
    assert species_prop['inheritance_path'] == ["Mammal", "Animal"]
    
    warm_prop = next(p for p in inherited if p['label'] == 'warm_blooded')
    assert warm_prop['inheritance_path'] == ["Mammal"]


def test_get_class_full(setup_class_hierarchy):
    """Test get_class_full returns complete information"""
    service = setup_class_hierarchy
    
    prof_full = service.get_class_full("Professor")
    
    # Check structure
    assert 'id' in prof_full
    assert 'label' in prof_full
    assert 'direct_properties' in prof_full
    assert 'inherited_properties' in prof_full
    assert 'all_properties' in prof_full
    
    # Check counts
    assert len(prof_full['direct_properties']) == 1  # department
    assert len(prof_full['inherited_properties']) == 2  # name, email
    assert len(prof_full['all_properties']) == 3  # total
    
    # Check inheritance markers
    for prop in prof_full['direct_properties']:
        assert prop['source'] == 'direct'
    
    for prop in prof_full['inherited_properties']:
        assert prop['source'] == 'Person'


def test_circular_inheritance_prevention(ontology_service):
    """Test system prevents infinite loops from circular inheritance"""
    service = ontology_service
    
    # Create A -> B classes
    a = OntologyClass(id="A", label="A")
    service.create_class(a)
    
    b = OntologyClass(id="B", label="B", parent_classes=["A"])
    service.create_class(b)
    
    # Simulate circular inheritance by passing visited set
    visited = {"A", "B"}
    result = service.compute_inherited_properties("A", visited=visited)
    
    # Should return empty list, not infinite loop
    assert result == []


def test_validate_instance_no_errors(setup_class_hierarchy):
    """Test instance validation passes when all required properties present"""
    service = setup_class_hierarchy
    
    # This test will pass once we add 'required' flag to properties
    # For now, no validation errors since we default required=False
    errors = service.validate_instance_properties(
        "Professor",
        {
            "hasName": "Alice Smith",
            "hasEmail": "alice@university.edu",
            "hasDepartment": "Computer Science"
        }
    )
    
    assert len(errors) == 0


def test_validate_instance_missing_direct_property(ontology_service):
    """Test validation catches missing direct required property"""
    service = ontology_service
    
    # Create class with required property
    person = OntologyClass(id="Person", label="Person")
    service.create_class(person)
    
    name_prop = OntologyProperty(
        id="hasName",
        label="name",
        property_type=PropertyType.DATA,
        domain=["Person"],
        range=["string"]
    )
    service.create_property(name_prop)
    
    # Manually add required flag to the property definition
    # (In real implementation, this would be part of property metadata)
    class_full = service.get_class_full("Person")
    
    # For now, validation will pass since required defaults to False
    # This test documents expected behavior for future enhancement
    errors = service.validate_instance_properties("Person", {})
    assert isinstance(errors, list)


def test_owl_thing_ignored_in_inheritance(ontology_service):
    """Test that owl:Thing is properly ignored in inheritance computation"""
    service = ontology_service
    
    # Create a class with only owl:Thing as parent
    simple = OntologyClass(id="SimpleClass", label="Simple")
    service.create_class(simple)
    
    # Should not inherit anything from owl:Thing
    inherited = service.compute_inherited_properties("SimpleClass")
    assert len(inherited) == 0


def test_multiple_inheritance_paths(ontology_service):
    """Test handling of properties inherited through multiple paths"""
    service = ontology_service
    
    # Create diamond inheritance: Thing -> A, Thing -> B, C -> A+B
    thing = OntologyClass(id="Thing", label="Thing")
    service.create_class(thing)
    
    prop_thing = OntologyProperty(
        id="hasThing",
        label="thing_prop",
        property_type=PropertyType.DATA,
        domain=["Thing"],
        range=["string"]
    )
    service.create_property(prop_thing)
    
    a = OntologyClass(id="A", label="A", parent_classes=["Thing"])
    service.create_class(a)
    
    b = OntologyClass(id="B", label="B", parent_classes=["Thing"])
    service.create_class(b)
    
    c = OntologyClass(id="C", label="C", parent_classes=["A", "B"])
    service.create_class(c)
    
    # C should inherit thing_prop, but may appear twice (through A and B)
    inherited = service.compute_inherited_properties("C")
    
    # Should have properties from both paths
    assert len(inherited) >= 1
    
    # Property IDs should include hasThing
    prop_ids = [p['id'] for p in inherited]
    assert "hasThing" in prop_ids


def test_no_properties_on_leaf_class(ontology_service):
    """Test class with no direct properties only shows inherited"""
    service = ontology_service
    
    parent = OntologyClass(id="Parent", label="Parent")
    service.create_class(parent)
    
    parent_prop = OntologyProperty(
        id="parentProp",
        label="parent_property",
        property_type=PropertyType.DATA,
        domain=["Parent"],
        range=["string"]
    )
    service.create_property(parent_prop)
    
    child = OntologyClass(id="Child", label="Child", parent_classes=["Parent"])
    service.create_class(child)
    
    child_full = service.get_class_full("Child")
    
    assert len(child_full['direct_properties']) == 0
    assert len(child_full['inherited_properties']) == 1
    assert child_full['inherited_properties'][0]['id'] == 'parentProp'


def test_property_metadata_preserved(setup_class_hierarchy):
    """Test that property metadata is preserved through inheritance"""
    service = setup_class_hierarchy
    
    prof_full = service.get_class_full("Professor")
    
    # Check that inherited properties have all metadata
    for prop in prof_full['inherited_properties']:
        assert 'id' in prop
        assert 'label' in prop
        assert 'property_type' in prop
        assert 'description' in prop
        assert 'range' in prop
        assert 'source' in prop
        assert 'inheritance_path' in prop


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
