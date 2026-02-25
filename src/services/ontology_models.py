"""
Ontology Models

Data models for ontology editor components including classes, properties,
instances, and reasoning results.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Set
from enum import Enum


class PropertyType(Enum):
    """Types of ontology properties"""
    OBJECT = "object"  # Relationships between instances
    DATA = "data"  # Literal values (strings, numbers, etc.)
    ANNOTATION = "annotation"  # Metadata annotations


class PropertyCharacteristic(Enum):
    """Property characteristics for reasoning"""
    FUNCTIONAL = "functional"  # Max one value per subject
    INVERSE_FUNCTIONAL = "inverse_functional"  # Max one value per object
    TRANSITIVE = "transitive"  # If A→B and B→C then A→C
    SYMMETRIC = "symmetric"  # If A→B then B→A
    ASYMMETRIC = "asymmetric"  # If A→B then not B→A
    REFLEXIVE = "reflexive"  # A→A for all A
    IRREFLEXIVE = "irreflexive"  # Not A→A for any A


@dataclass
class OntologyClass:
    """
    Represents an ontology class (concept)
    
    Similar to OWL classes or RDFS classes
    """
    id: str
    label: str
    description: Optional[str] = None
    parent_classes: List[str] = field(default_factory=list)  # Direct superclasses
    equivalent_classes: List[str] = field(default_factory=list)
    disjoint_classes: List[str] = field(default_factory=list)  # Cannot overlap
    properties: Dict[str, Any] = field(default_factory=dict)  # Metadata
    annotations: Dict[str, str] = field(default_factory=dict)
    is_abstract: bool = False  # Cannot have direct instances
    
    def __post_init__(self):
        if not self.label:
            self.label = self.id


@dataclass
class OntologyProperty:
    """
    Represents an ontology property (relationship or attribute)
    
    Similar to OWL object/data properties or RDF predicates
    """
    id: str
    label: str
    property_type: PropertyType
    description: Optional[str] = None
    domain: List[str] = field(default_factory=list)  # Valid subject classes
    range: List[str] = field(default_factory=list)  # Valid object classes/datatypes
    parent_properties: List[str] = field(default_factory=list)  # Super-properties
    inverse_of: Optional[str] = None  # Inverse property
    characteristics: Set[PropertyCharacteristic] = field(default_factory=set)
    annotations: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.label:
            self.label = self.id
        if isinstance(self.property_type, str):
            self.property_type = PropertyType(self.property_type)


@dataclass
class OntologyInstance:
    """
    Represents an instance (individual) of ontology classes
    
    Similar to OWL individuals or RDF resources
    """
    id: str
    label: str
    class_ids: List[str] = field(default_factory=list)  # Classes this belongs to
    properties: Dict[str, Any] = field(default_factory=dict)  # Property values
    annotations: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.label:
            self.label = self.id


@dataclass
class ClassHierarchy:
    """
    Represents a class hierarchy tree node
    """
    class_id: str
    label: str
    parent_id: Optional[str] = None
    children: List['ClassHierarchy'] = field(default_factory=list)
    instance_count: int = 0
    depth: int = 0


@dataclass
class PropertyHierarchy:
    """
    Represents a property hierarchy tree node
    """
    property_id: str
    label: str
    property_type: PropertyType
    parent_id: Optional[str] = None
    children: List['PropertyHierarchy'] = field(default_factory=list)
    usage_count: int = 0


@dataclass
class ReasoningResult:
    """
    Results from reasoning/inference operations
    """
    consistent: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    inferred_relationships: List[Dict[str, Any]] = field(default_factory=list)
    inferred_types: Dict[str, List[str]] = field(default_factory=dict)
    subclass_closure: Dict[str, Set[str]] = field(default_factory=dict)
    reasoning_time: float = 0.0


@dataclass
class OntologyStats:
    """
    Statistics about an ontology
    """
    total_classes: int = 0
    total_properties: int = 0
    total_instances: int = 0
    total_object_properties: int = 0
    total_data_properties: int = 0
    total_annotation_properties: int = 0
    max_hierarchy_depth: int = 0
    total_axioms: int = 0
    consistency_status: str = "unknown"


@dataclass
class OntologyMetadata:
    """
    Metadata about an ontology
    """
    ontology_id: str
    version: str = "1.0"
    title: str = ""
    description: str = ""
    authors: List[str] = field(default_factory=list)
    created: Optional[str] = None
    modified: Optional[str] = None
    license: Optional[str] = None
    imports: List[str] = field(default_factory=list)
    namespaces: Dict[str, str] = field(default_factory=dict)


@dataclass
class OntologySearchResult:
    """
    Search result for ontology elements
    """
    element_type: str  # 'class', 'property', 'instance'
    element_id: str
    label: str
    description: Optional[str] = None
    match_score: float = 0.0
    matched_fields: List[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    """
    Results from ontology validation
    """
    valid: bool
    errors: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_error(self, message: str, element_id: Optional[str] = None, 
                  error_type: str = "validation"):
        """Add a validation error"""
        self.errors.append({
            "message": message,
            "element_id": element_id,
            "type": error_type
        })
        self.valid = False
    
    def add_warning(self, message: str, element_id: Optional[str] = None,
                    warning_type: str = "validation"):
        """Add a validation warning"""
        self.warnings.append({
            "message": message,
            "element_id": element_id,
            "type": warning_type
        })


# Datatype constants for data properties
class XSDDatatype:
    """Common XML Schema datatypes for data properties"""
    STRING = "xsd:string"
    INTEGER = "xsd:integer"
    FLOAT = "xsd:float"
    DOUBLE = "xsd:double"
    BOOLEAN = "xsd:boolean"
    DATE = "xsd:date"
    DATETIME = "xsd:dateTime"
    TIME = "xsd:time"
    ANY_URI = "xsd:anyURI"
