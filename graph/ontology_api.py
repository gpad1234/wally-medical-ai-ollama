#!/usr/bin/env python3
"""
Ontology Editor API Server

Flask REST API for the ontology editor application.
Provides endpoints for class, property, and instance management.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import logging
from datetime import datetime
from typing import Dict, Any
from src.services.ontology_service import OntologyService
from src.services.graph_pagination_service import GraphPaginationService
from src.services.ontology_models import (
    OntologyClass,
    OntologyProperty,
    OntologyInstance,
    PropertyType,
    PropertyCharacteristic,
)
from src.services.base_service import (
    NodeNotFoundError,
    ValidationError,
    InvalidOperationError,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize ontology service (lazy initialization to avoid startup hang)
ontology_service = None
pagination_service = None

def init_demo_data(service):
    """Initialize demo data if ontology is empty"""
    from src.services.ontology_models import (
        OntologyClass, OntologyProperty, OntologyInstance,
        PropertyType, XSDDatatype
    )
    
    # Check if already initialized (more than just owl:Thing)
    if len(service.get_all_classes()) > 1:
        logger.info("Demo data already exists, skipping initialization")
        return
    
    logger.info("Initializing demo data...")
    
    try:
        # Create classes
        service.create_class(OntologyClass(
            id="demo:Person", label="Person",
            description="A human being",
            parent_classes=["owl:Thing"]
        ))
        service.create_class(OntologyClass(
            id="demo:Professor", label="Professor",
            description="A university professor",
            parent_classes=["demo:Person"]
        ))
        service.create_class(OntologyClass(
            id="demo:Student", label="Student",
            description="A university student",
            parent_classes=["demo:Person"]
        ))
        service.create_class(OntologyClass(
            id="demo:Employee", label="Employee",
            description="An employee",
            parent_classes=["demo:Person"]
        ))
        
        # Create properties
        service.create_property(OntologyProperty(
            id="demo:name", label="name",
            property_type=PropertyType.DATA,
            domain=["demo:Person"],
            range=[str(XSDDatatype.STRING)],
            annotations={"required": "true"}
        ))
        service.create_property(OntologyProperty(
            id="demo:email", label="email",
            property_type=PropertyType.DATA,
            domain=["demo:Person"],
            range=[str(XSDDatatype.STRING)],
            annotations={"required": "true"}
        ))
        service.create_property(OntologyProperty(
            id="demo:department", label="department",
            property_type=PropertyType.DATA,
            domain=["demo:Professor"],
            range=[str(XSDDatatype.STRING)],
            annotations={"required": "true"}
        ))
        service.create_property(OntologyProperty(
            id="demo:student_id", label="student_id",
            property_type=PropertyType.DATA,
            domain=["demo:Student"],
            range=[str(XSDDatatype.STRING)],
            annotations={"required": "true"}
        ))
        
        # Create instances
        service.create_instance(OntologyInstance(
            id="demo:prof_smith",
            label="Professor Smith",
            class_ids=["demo:Professor"],
            properties={
                "demo:name": "Dr. John Smith",
                "demo:email": "john.smith@university.edu",
                "demo:department": "Computer Science"
            }
        ))
        service.create_instance(OntologyInstance(
            id="demo:student_jones",
            label="Student Jones",
            class_ids=["demo:Student"],
            properties={
                "demo:name": "Alice Jones",
                "demo:email": "alice.jones@university.edu",
                "demo:student_id": "S12345"
            }
        ))
        
        logger.info(f"Demo data initialized: {len(service.get_all_classes())} classes")
    except Exception as e:
        logger.warning(f"Error initializing demo data: {e}")

def get_ontology_service():
    """Get or create ontology service instance"""
    global ontology_service
    if ontology_service is None:
        logger.info("Initializing ontology service...")
        ontology_service = OntologyService()
        logger.info("Ontology service initialized successfully")
        init_demo_data(ontology_service)
    return ontology_service


def get_pagination_service():
    """Get or create pagination service instance"""
    global pagination_service
    if pagination_service is None:
        logger.info("Initializing pagination service...")
        pagination_service = GraphPaginationService(get_ontology_service().graph)
        logger.info("Pagination service initialized successfully")
    return pagination_service


# ============================================================================
# Helper Functions
# ============================================================================

def success_response(data: Any, message: str = "Success") -> Dict:
    """Create success response"""
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }


def error_response(error: str, status_code: int = 400) -> tuple:
    """Create error response"""
    return jsonify({
        "success": False,
        "error": error,
        "timestamp": datetime.utcnow().isoformat()
    }), status_code


# ============================================================================
# Class Endpoints
# ============================================================================

@app.route('/api/ontology/classes', methods=['GET'])
def get_classes():
    """Get all ontology classes"""
    try:
        classes = get_ontology_service().get_all_classes()
        return jsonify(success_response([
            {
                "id": c.id,
                "label": c.label,
                "description": c.description,
                "parent_classes": c.parent_classes,
                "is_abstract": c.is_abstract
            } for c in classes
        ]))
    except Exception as e:
        logger.error(f"Error getting classes: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/classes/<class_id>', methods=['GET'])
def get_class(class_id: str):
    """Get specific class"""
    try:
        class_obj = get_ontology_service().get_class(class_id)
        return jsonify(success_response({
            "id": class_obj.id,
            "label": class_obj.label,
            "description": class_obj.description,
            "parent_classes": class_obj.parent_classes,
            "equivalent_classes": class_obj.equivalent_classes,
            "disjoint_classes": class_obj.disjoint_classes,
            "is_abstract": class_obj.is_abstract
        }))
    except NodeNotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        logger.error(f"Error getting class {class_id}: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/classes', methods=['POST'])
def create_class():
    """Create new class"""
    try:
        data = request.get_json()
        
        class_obj = OntologyClass(
            id=data['id'],
            label=data.get('label', data['id']),
            description=data.get('description'),
            parent_classes=data.get('parent_classes', []),
            equivalent_classes=data.get('equivalent_classes', []),
            disjoint_classes=data.get('disjoint_classes', []),
            is_abstract=data.get('is_abstract', False)
        )
        
        created = get_ontology_service().create_class(class_obj)
        
        return jsonify(success_response({
            "id": created.id,
            "label": created.label,
            "description": created.description,
            "parent_classes": created.parent_classes
        }, "Class created successfully"))
    
    except ValidationError as e:
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error creating class: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/classes/<class_id>', methods=['DELETE'])
def delete_class(class_id: str):
    """Delete a class"""
    try:
        force = request.args.get('force', 'false').lower() == 'true'
        get_ontology_service().delete_class(class_id, force=force)
        return jsonify(success_response(None, f"Class '{class_id}' deleted"))
    except (NodeNotFoundError, InvalidOperationError) as e:
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error deleting class {class_id}: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/classes/<class_id>/subclasses', methods=['GET'])
def get_subclasses(class_id: str):
    """Get subclasses of a class"""
    try:
        direct_only = request.args.get('direct', 'false').lower() == 'true'
        subclasses = get_ontology_service().get_subclasses(class_id, direct_only=direct_only)
        return jsonify(success_response([
            {"id": c.id, "label": c.label, "description": c.description}
            for c in subclasses
        ]))
    except Exception as e:
        logger.error(f"Error getting subclasses: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/classes/<class_id>/superclasses', methods=['GET'])
def get_superclasses(class_id: str):
    """Get superclasses of a class"""
    try:
        direct_only = request.args.get('direct', 'false').lower() == 'true'
        superclasses = get_ontology_service().get_superclasses(class_id, direct_only=direct_only)
        return jsonify(success_response([
            {"id": c.id, "label": c.label, "description": c.description}
            for c in superclasses
        ]))
    except Exception as e:
        logger.error(f"Error getting superclasses: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/classes/<class_id>/full', methods=['GET'])
def get_class_full(class_id: str):
    """Get class with complete inheritance information"""
    try:
        class_full = get_ontology_service().get_class_full(class_id)
        return jsonify(success_response(class_full))
    except NodeNotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        logger.error(f"Error getting full class info: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/hierarchy', methods=['GET'])
def get_hierarchy():
    """Get class hierarchy tree"""
    try:
        root_id = request.args.get('root', 'owl:Thing')
        hierarchy = get_ontology_service().get_class_hierarchy(root_id)
        
        def serialize_hierarchy(node):
            return {
                "class_id": node.class_id,
                "label": node.label,
                "parent_id": node.parent_id,
                "instance_count": node.instance_count,
                "depth": node.depth,
                "children": [serialize_hierarchy(child) for child in node.children]
            }
        
        return jsonify(success_response(serialize_hierarchy(hierarchy)))
    except Exception as e:
        logger.error(f"Error getting hierarchy: {e}", exc_info=True)
        return error_response(str(e), 500)


# ============================================================================
# Property Endpoints
# ============================================================================

@app.route('/api/ontology/properties', methods=['GET'])
def get_properties():
    """Get all ontology properties"""
    try:
        properties = get_ontology_service().get_all_properties()
        return jsonify(success_response([
            {
                "id": p.id,
                "label": p.label,
                "property_type": p.property_type.value,
                "description": p.description,
                "domain": p.domain,
                "range": p.range
            } for p in properties
        ]))
    except Exception as e:
        logger.error(f"Error getting properties: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/properties/<property_id>', methods=['GET'])
def get_property(property_id: str):
    """Get specific property"""
    try:
        prop = get_ontology_service().get_property(property_id)
        return jsonify(success_response({
            "id": prop.id,
            "label": prop.label,
            "property_type": prop.property_type.value,
            "description": prop.description,
            "domain": prop.domain,
            "range": prop.range,
            "inverse_of": prop.inverse_of,
            "characteristics": [c.value for c in prop.characteristics]
        }))
    except NodeNotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        logger.error(f"Error getting property {property_id}: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/properties', methods=['POST'])
def create_property():
    """Create new property"""
    try:
        data = request.get_json()
        
        # Parse property type
        prop_type = PropertyType(data.get('property_type', 'object'))
        
        # Parse characteristics
        characteristics = set()
        for char in data.get('characteristics', []):
            try:
                characteristics.add(PropertyCharacteristic(char))
            except ValueError:
                pass
        
        prop_obj = OntologyProperty(
            id=data['id'],
            label=data.get('label', data['id']),
            property_type=prop_type,
            description=data.get('description'),
            domain=data.get('domain', []),
            range=data.get('range', []),
            inverse_of=data.get('inverse_of'),
            characteristics=characteristics
        )
        
        created = get_ontology_service().create_property(prop_obj)
        
        return jsonify(success_response({
            "id": created.id,
            "label": created.label,
            "property_type": created.property_type.value,
            "description": created.description
        }, "Property created successfully"))
    
    except ValidationError as e:
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error creating property: {e}", exc_info=True)
        return error_response(str(e), 500)


# ============================================================================
# Instance Endpoints
# ============================================================================

@app.route('/api/ontology/instances', methods=['POST'])
def create_instance():
    """Create new instance"""
    try:
        data = request.get_json()
        
        instance_obj = OntologyInstance(
            id=data['id'],
            label=data.get('label', data['id']),
            class_ids=data.get('class_ids', []),
            properties=data.get('properties', {})
        )
        
        # Validate properties against class requirements (including inheritance)
        validation_errors = []
        for class_id in instance_obj.class_ids:
            try:
                errors = get_ontology_service().validate_instance_properties(
                    class_id, 
                    instance_obj.properties
                )
                validation_errors.extend(errors)
            except Exception as e:
                logger.warning(f"Could not validate against class {class_id}: {e}")
        
        if validation_errors:
            return jsonify({
                "success": False,
                "error": "Validation failed",
                "details": validation_errors,
                "timestamp": datetime.utcnow().isoformat()
            }), 422
        
        created = get_ontology_service().create_instance(instance_obj)
        
        return jsonify(success_response({
            "id": created.id,
            "label": created.label,
            "class_ids": created.class_ids,
            "properties": created.properties
        }, "Instance created successfully"))
    
    except ValidationError as e:
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error creating instance: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/instances/<instance_id>', methods=['GET'])
def get_instance(instance_id: str):
    """Get specific instance"""
    try:
        inst = get_ontology_service().get_instance(instance_id)
        return jsonify(success_response({
            "id": inst.id,
            "label": inst.label,
            "class_ids": inst.class_ids,
            "properties": inst.properties
        }))
    except NodeNotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        logger.error(f"Error getting instance {instance_id}: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/classes/<class_id>/instances', methods=['GET'])
def get_class_instances(class_id: str):
    """Get all instances of a class"""
    try:
        direct_only = request.args.get('direct', 'true').lower() == 'true'
        instances = get_ontology_service().get_instances_of_class(class_id, direct_only=direct_only)
        return jsonify(success_response([
            {
                "id": i.id,
                "label": i.label,
                "class_ids": i.class_ids
            } for i in instances
        ]))
    except Exception as e:
        logger.error(f"Error getting instances: {e}", exc_info=True)
        return error_response(str(e), 500)


# ============================================================================
# Medical AI Ontology Endpoint
# ============================================================================

@app.route('/api/ontology/medical', methods=['GET'])
def get_medical_ontology():
    """
    Parse sample_data/medical_ontology.ttl and return the knowledge graph
    as JSON in the shape expected by MedicalDiagnosisAI.jsx:
    { diseases, symptoms, treatments, hierarchy }
    """
    import os
    from rdflib import Graph, Namespace, RDF, RDFS, Literal
    from rdflib.namespace import OWL

    TTL_PATH = os.path.join(os.path.dirname(__file__), 'sample_data', 'medical_ontology.ttl')
    if not os.path.exists(TTL_PATH):
        return error_response('medical_ontology.ttl not found', 404)

    try:
        g = Graph()
        g.parse(TTL_PATH, format='turtle')

        MED   = Namespace('http://wally.io/medical#')
        RDFS_LABEL = RDFS.label

        def str_val(node):
            return str(node) if node else None

        def get_id(subject):
            ids = list(g.objects(subject, MED.id))
            return str_val(ids[0]) if ids else None

        def get_label(subject):
            labels = list(g.objects(subject, RDFS_LABEL))
            return str_val(labels[0]) if labels else None

        # ---- Symptoms -------------------------------------------------------
        symptoms = {}
        for s in g.subjects(RDF.type, MED.Symptom):
            sid = get_id(s)
            if not sid:
                continue
            label = get_label(s)
            weights = {}
            for bnode in g.objects(s, MED.hasSymptomWeight):
                disease_ids = list(g.objects(bnode, MED.weightDisease))
                weight_vals = list(g.objects(bnode, MED.weightValue))
                if disease_ids and weight_vals:
                    weights[str_val(disease_ids[0])] = float(weight_vals[0])
            symptoms[sid] = {'label': label, 'weights': weights}

        # ---- Treatments -----------------------------------------------------
        treatments = {}
        for s in g.subjects(RDF.type, MED.Treatment):
            tid = get_id(s)
            if not tid:
                continue
            treat_types = list(g.objects(s, MED.treatType))
            treatments[tid] = {
                'label': get_label(s),
                'type': str_val(treat_types[0]) if treat_types else 'general'
            }

        # ---- Diseases -------------------------------------------------------
        diseases = {}
        for s in g.subjects(RDF.type, MED.Disease):
            did = get_id(s)
            if not did:
                continue
            parents   = list(g.objects(s, MED.parent))
            severities = list(g.objects(s, MED.severity))
            descs     = list(g.objects(s, MED.description))

            # hasSymptom -> list of symptom compact IDs
            sym_ids = []
            for sym_node in g.objects(s, MED.hasSymptom):
                sym_id = get_id(sym_node)
                if sym_id:
                    sym_ids.append(sym_id)

            # hasTreatment -> list of treatment compact IDs
            treat_ids = []
            for t_node in g.objects(s, MED.hasTreatment):
                t_id = get_id(t_node)
                if t_id:
                    treat_ids.append(t_id)

            diseases[did] = {
                'label':       get_label(s),
                'parent':      str_val(parents[0]) if parents else None,
                'severity':    str_val(severities[0]) if severities else 'moderate',
                'description': str_val(descs[0]) if descs else '',
                'symptoms':    sym_ids,
                'treatments':  treat_ids,
                # Disease Ontology enrichment
                'doid':        str_val(next(g.objects(s, MED.doid),   None)),
                'officialDef': str_val(next(g.objects(s, RDFS.comment), None)),
                'synonyms':    [str_val(v) for v in g.objects(s, MED.synonym)],
                'icd10Refs':   [str_val(v) for v in g.objects(s, MED.icd10Ref)],
                'meshRefs':    [str_val(v) for v in g.objects(s, MED.meshRef)],
            }

        # ---- Hierarchy -------------------------------------------------------
        hierarchy = {}
        for s in g.subjects(RDF.type, MED.HierarchyNode):
            hid = get_id(s)
            if not hid:
                continue
            parents = list(g.objects(s, MED.parent))
            hierarchy[hid] = {
                'label':  get_label(s),
                'parent': str_val(parents[0]) if parents else 'owl:Disease'
            }

        return jsonify(success_response({
            'diseases':   diseases,
            'symptoms':   symptoms,
            'treatments': treatments,
            'hierarchy':  hierarchy,
            'source':     'sample_data/medical_ontology.ttl',
        }, 'Medical ontology loaded successfully'))

    except Exception as e:
        logger.error(f"Error parsing medical ontology: {e}", exc_info=True)
        return error_response(f'Failed to parse medical_ontology.ttl: {str(e)}', 500)


@app.route('/api/ontology/medical/graph', methods=['GET'])
def get_medical_graph():
    """
    Parse medical_ontology.ttl and return OWL classes + individuals
    in the shape expected by GraphView / OntologyDemo.
    Returns: { classes: [...], instances: [...], source, summary }
    """
    from rdflib import Graph as RDFGraph, Namespace, RDF, RDFS, OWL, Literal, BNode
    import os

    TTL_PATH = os.path.join(os.path.dirname(__file__), 'sample_data', 'medical_ontology.ttl')
    if not os.path.exists(TTL_PATH):
        return error_response('medical_ontology.ttl not found', 404)

    try:
        g = RDFGraph()
        g.parse(TTL_PATH, format='turtle')

        # Build prefix → namespace map for compact IDs
        ns_map = {str(ns): prefix for prefix, ns in g.namespaces() if prefix}

        def compact_id(uri):
            s = str(uri)
            for ns_str, prefix in ns_map.items():
                if s.startswith(ns_str):
                    return f"{prefix}:{s[len(ns_str):]}"
            return s

        def get_label(uri):
            for lbl in g.objects(uri, RDFS.label):
                return str(lbl)
            s = str(uri)
            return s.split('#')[-1].split('/')[-1]

        # ---- Per-class property definitions (domain knowledge) ----
        class_props = {
            'med:Disease': [
                {'id': 'med:id',          'label': 'id',          'required': True,  'inherited': False},
                {'id': 'med:severity',    'label': 'severity',    'required': False, 'inherited': False},
                {'id': 'med:description', 'label': 'description', 'required': False, 'inherited': False},
                {'id': 'med:hasTreatment','label': 'hasTreatment','required': False, 'inherited': False},
                {'id': 'med:hasSymptom',  'label': 'hasSymptom',  'required': False, 'inherited': False},
            ],
            'med:Symptom': [
                {'id': 'med:id',               'label': 'id',               'required': True,  'inherited': False},
                {'id': 'med:hasSymptomWeight',  'label': 'hasSymptomWeight', 'required': False, 'inherited': False},
            ],
            'med:Treatment': [
                {'id': 'med:id',       'label': 'id',       'required': True,  'inherited': False},
                {'id': 'med:treatType','label': 'treatType','required': False, 'inherited': False},
            ],
            'med:HierarchyNode': [
                {'id': 'med:id',    'label': 'id',    'required': True,  'inherited': False},
                {'id': 'med:parent','label': 'parent','required': False, 'inherited': False},
            ],
        }

        # ---- Build class list ----
        owl_class_uris = list(g.subjects(RDF.type, OWL.Class))

        classes = [{
            'id': 'owl:Thing',
            'label': 'Thing',
            'description': 'Root of all OWL classes',
            'parent_classes': [],
            'direct_properties': [],
            'all_properties': []
        }]

        for cls_uri in owl_class_uris:
            if isinstance(cls_uri, BNode):
                continue
            cid = compact_id(cls_uri)
            parents = []
            for sup in g.objects(cls_uri, RDFS.subClassOf):
                if not isinstance(sup, BNode):
                    parents.append(compact_id(sup))
            if not parents:
                parents = ['owl:Thing']

            desc = next((str(d) for d in g.objects(cls_uri, RDFS.comment)), None)
            direct_props = class_props.get(cid, [])

            classes.append({
                'id': cid,
                'label': get_label(cls_uri),
                'description': desc or f'A {get_label(cls_uri)} in the medical ontology',
                'parent_classes': parents,
                'direct_properties': direct_props,
                'all_properties': direct_props,
            })

        # ---- Build instance list ----
        instances = []
        for cls_uri in owl_class_uris:
            if isinstance(cls_uri, BNode):
                continue
            cid = compact_id(cls_uri)
            for inst_uri in g.subjects(RDF.type, cls_uri):
                if isinstance(inst_uri, BNode):
                    continue
                iid = compact_id(inst_uri)
                ilabel = get_label(inst_uri)
                props = {}
                for pred, obj in g.predicate_objects(inst_uri):
                    if pred in (RDF.type, RDFS.label):
                        continue
                    pid = compact_id(pred)
                    if isinstance(obj, BNode):
                        for bp, bv in g.predicate_objects(obj):
                            props[f"{pid}.{compact_id(bp)}"] = str(bv)
                    elif isinstance(obj, Literal):
                        props[pid] = str(obj)
                    else:
                        props[pid] = compact_id(obj)
                instances.append({'id': iid, 'label': ilabel, 'classId': cid, 'properties': props})

        return jsonify(success_response({
            'classes':   classes,
            'instances': instances,
            'source':    'sample_data/medical_ontology.ttl',
            'summary':   {'class_count': len(classes), 'instance_count': len(instances)}
        }, 'Medical ontology graph loaded successfully'))

    except Exception as e:
        logger.error(f"Error parsing medical ontology graph: {e}", exc_info=True)
        return error_response(f'Failed to build medical graph: {str(e)}', 500)


# ============================================================================
# Reasoning & Analysis Endpoints
# ============================================================================

@app.route('/api/ontology/reasoning/consistency', methods=['GET'])
def check_consistency():
    """Check ontology consistency"""
    try:
        result = get_ontology_service().check_consistency()
        return jsonify(success_response({
            "consistent": result.consistent,
            "errors": result.errors,
            "warnings": result.warnings,
            "reasoning_time": result.reasoning_time
        }))
    except Exception as e:
        logger.error(f"Error checking consistency: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/statistics', methods=['GET'])
def get_statistics():
    """Get ontology statistics"""
    try:
        stats = get_ontology_service().get_statistics()
        return jsonify(success_response({
            "total_classes": stats.total_classes,
            "total_properties": stats.total_properties,
            "total_instances": stats.total_instances,
            "total_object_properties": stats.total_object_properties,
            "total_data_properties": stats.total_data_properties,
            "total_annotation_properties": stats.total_annotation_properties,
            "max_hierarchy_depth": stats.max_hierarchy_depth
        }))
    except Exception as e:
        logger.error(f"Error getting statistics: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/validate', methods=['GET'])
def validate_ontology():
    """Validate ontology structure"""
    try:
        result = get_ontology_service().validate_ontology()
        return jsonify(success_response({
            "valid": result.valid,
            "errors": result.errors,
            "warnings": result.warnings
        }))
    except Exception as e:
        logger.error(f"Error validating ontology: {e}", exc_info=True)
        return error_response(str(e), 500)


# ============================================================================
# Import/Export Endpoints
# ============================================================================

@app.route('/api/ontology/export', methods=['GET'])
def export_ontology():
    """Export ontology to RDF format"""
    try:
        format_type = request.args.get('format', 'xml')
        rdf_content = get_ontology_service().export_to_rdf(format=format_type)

        # Set appropriate content type
        content_types = {
            "xml": "application/rdf+xml",
            "turtle": "text/turtle",
            "ttl": "text/turtle",
            "n3": "text/n3",
            "nt": "application/n-triples"
        }
        content_type = content_types.get(format_type.lower(), "application/rdf+xml")

        # Return raw RDF content
        from flask import Response
        return Response(rdf_content, mimetype=content_type)
    except Exception as e:
        logger.error(f"Error exporting ontology: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/import', methods=['POST'])
def import_ontology():
    """Import ontology from RDF format"""
    try:
        # Get file from request
        if 'file' in request.files:
            file = request.files['file']
            rdf_content = file.read().decode('utf-8')

            # Detect format from file extension
            filename = file.filename.lower()
            if filename.endswith('.ttl') or filename.endswith('.turtle'):
                format_type = 'turtle'
            elif filename.endswith('.n3'):
                format_type = 'n3'
            elif filename.endswith('.nt'):
                format_type = 'nt'
            else:  # .rdf, .owl, .xml
                format_type = 'xml'
        else:
            # Get from JSON body
            data = request.get_json()
            rdf_content = data.get('content')
            format_type = data.get('format', 'xml')

        if not rdf_content:
            return error_response("No RDF content provided", 400)

        clear_existing = request.args.get('clear', 'false').lower() == 'true'

        # Import the RDF
        counts = get_ontology_service().import_from_rdf(
            rdf_content=rdf_content,
            format=format_type,
            clear_existing=clear_existing
        )

        return jsonify(success_response(counts, "Ontology imported successfully"))

    except ValidationError as e:
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error importing ontology: {e}", exc_info=True)
        return error_response(str(e), 500)


# ============================================================================
# Medical AI — Ollama LLM Diagnosis (Sprint 1)
# ============================================================================

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    """
    POST /api/diagnose
    Body: { "symptoms": ["Fever", "Cough", ...] }
    Returns: { diagnosis, reasoning, model_used }

    Builds a concise prompt from the medical ontology (diseases + symptoms)
    and forwards it to the local Ollama llama3.2:3b model.
    """
    import ollama
    import os
    from rdflib import Graph as RDFGraph, Namespace, RDF, RDFS

    data = request.get_json(silent=True) or {}
    symptoms = data.get('symptoms', [])

    if not symptoms:
        return error_response('No symptoms provided. Send {"symptoms": ["Fever","Cough"]}', 400)

    # ---- Load the medical ontology for context ---------------------------
    TTL_PATH = os.path.join(os.path.dirname(__file__), 'sample_data', 'medical_ontology.ttl')
    disease_context = ""
    if os.path.exists(TTL_PATH):
        try:
            g = RDFGraph()
            g.parse(TTL_PATH, format='turtle')
            MED = Namespace('http://wally.io/medical#')

            lines = []
            for s in g.subjects(RDF.type, MED.Disease):
                disease_id = next(g.objects(s, MED.id), None)
                label = next(g.objects(s, RDFS.label), None)
                severity = next(g.objects(s, MED.severity), None)
                sym_labels = []
                for sym_node in g.objects(s, MED.hasSymptom):
                    sym_label = next(g.objects(sym_node, RDFS.label), None)
                    if sym_label:
                        sym_labels.append(str(sym_label))
                if label:
                    lines.append(
                        f"- {label} (severity: {severity or 'unknown'}): symptoms include {', '.join(sym_labels)}"
                    )
            disease_context = "\n".join(lines)
        except Exception as e:
            logger.warning(f"Could not load TTL for diagnose prompt: {e}")

    if not disease_context:
        disease_context = (
            "- Common Cold (mild): Runny Nose, Sore Throat, Cough, Sneezing, Fatigue\n"
            "- Influenza (moderate): Fever, Cough, Fatigue, Body Aches, Headache, Sore Throat\n"
            "- Pneumonia (severe): Fever, Cough, Chest Pain, Shortness of Breath, Fatigue\n"
            "- Bronchitis (moderate): Cough, Mucus, Chest Discomfort, Fatigue\n"
            "- Gastroenteritis (moderate): Nausea, Vomiting, Diarrhea, Abdominal Pain, Fever\n"
            "- Migraine (moderate): Severe Headache, Nausea, Light Sensitivity, Sound Sensitivity\n"
            "- Hypertension (moderate): Headache, Dizziness, Chest Pain"
        )

    symptom_list = ", ".join(symptoms)
    system_prompt = (
        "You are a medical AI assistant using an ontology-based knowledge graph. "
        "Your role is educational — never replace real medical advice. "
        "Given the patient symptoms and the knowledge base of diseases, "
        "reason step by step to suggest the most likely conditions, explain why, "
        "and note recommended next steps. Be concise."
    )
    user_prompt = (
        f"Knowledge base (diseases and their typical symptoms):\n{disease_context}\n\n"
        f"Patient symptoms: {symptom_list}\n\n"
        "Please provide:\n"
        "1. Most likely diagnosis (and confidence reasoning)\n"
        "2. Brief reasoning trace using the ontology relationships\n"
        "3. Recommended next steps"
    )

    # ---- Call Ollama -------------------------------------------------------
    try:
        response = ollama.chat(
            model='llama3.2:3b',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user',   'content': user_prompt},
            ]
        )
        llm_text = response['message']['content']
        model_used = response.get('model', 'llama3.2:3b')
    except Exception as e:
        logger.error(f"Ollama error: {e}", exc_info=True)
        return error_response(
            f"Ollama unavailable: {str(e)}. Make sure ollama is running and llama3.2:3b is pulled.",
            503
        )

    return jsonify(success_response({
        'diagnosis': llm_text,
        'reasoning': f'LLM-based reasoning over medical ontology ({len(symptoms)} symptoms analyzed)',
        'model_used': model_used,
        'symptoms_received': symptoms,
    }, 'LLM diagnosis complete'))


# ============================================================================
# Graph Pagination Endpoints
# ============================================================================

@app.route('/api/ontology/graph/nodes', methods=['GET'])
def get_paginated_nodes():
    """Get paginated list of nodes
    
    Query Parameters:
        skip (int): Number of nodes to skip (default: 0)
        limit (int): Maximum nodes to return (default: 50)
        type (str): Optional node type filter (e.g., 'owl:Class')
        search (str): Optional search query
    
    Returns:
        JSON with nodes, edges, pagination metadata
    """
    try:
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 50))
        node_type = request.args.get('type')
        search_query = request.args.get('search')
        
        result = get_pagination_service().get_page(
            skip=skip,
            limit=limit,
            node_type=node_type,
            search_query=search_query
        )
        
        return jsonify(success_response(result))
        
    except Exception as e:
        logger.error(f"Error getting paginated nodes: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/graph/viewport', methods=['POST'])
def get_viewport():
    """Get fish-eye viewport centered on a node
    
    Request Body (JSON):
        center_node (str): ID of the center node
        radius (int): Number of hops from center (default: 2)
        limit (int): Maximum nodes to return (default: 50)
    
    Returns:
        JSON with nodes, edges, distance levels
    """
    try:
        data = request.get_json()
        
        if not data or 'center_node' not in data:
            return error_response("Missing 'center_node' in request body", 400)
        
        center_node = data['center_node']
        radius = data.get('radius', 2)
        limit = data.get('limit', 50)
        
        result = get_pagination_service().get_viewport(
            center_id=center_node,
            radius=radius,
            limit=limit
        )
        
        return jsonify(success_response(result))
        
    except Exception as e:
        logger.error(f"Error getting viewport: {e}", exc_info=True)
        return error_response(str(e), 500)


@app.route('/api/ontology/graph/neighbors/<node_id>', methods=['GET'])
def get_neighbors(node_id):
    """Get immediate neighbors of a node
    
    Path Parameters:
        node_id (str): ID of the node
    
    Query Parameters:
        depth (int): Number of hops (default: 1)
    
    Returns:
        JSON with neighbor nodes and connecting edges
    """
    try:
        depth = int(request.args.get('depth', 1))
        
        result = get_pagination_service().get_neighbors(
            node_id=node_id,
            depth=depth
        )
        
        return jsonify(success_response(result))
        
    except Exception as e:
        logger.error(f"Error getting neighbors: {e}", exc_info=True)
        return error_response(str(e), 500)


# ============================================================================
# Utility Endpoints
# ============================================================================

@app.route('/api/ontology/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify(success_response({
        "status": "healthy",
        "service": "Ontology Editor API",
        "version": "1.0.0"
    }))


@app.route('/')
def index():
    """Render main page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ontology Editor API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #2c3e50; }
            .endpoint { background: #f8f9fa; padding: 10px; margin: 10px 0; border-left: 3px solid #3498db; }
            code { background: #e9ecef; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🧠 Ontology Editor API</h1>
        <p>RESTful API for semantic ontology management</p>
        
        <h2>Available Endpoints</h2>
        
        <div class="endpoint">
            <strong>GET /api/ontology/classes</strong> - List all classes
        </div>
        <div class="endpoint">
            <strong>POST /api/ontology/classes</strong> - Create new class
        </div>
        <div class="endpoint">
            <strong>GET /api/ontology/classes/{id}</strong> - Get class details
        </div>
        <div class="endpoint">
            <strong>GET /api/ontology/hierarchy</strong> - Get class hierarchy
        </div>
        <div class="endpoint">
            <strong>GET /api/ontology/properties</strong> - List all properties
        </div>
        <div class="endpoint">
            <strong>POST /api/ontology/properties</strong> - Create new property
        </div>
        <div class="endpoint">
            <strong>POST /api/ontology/instances</strong> - Create new instance
        </div>
        <div class="endpoint">
            <strong>GET /api/ontology/statistics</strong> - Get ontology stats
        </div>
        <div class="endpoint">
            <strong>GET /api/ontology/reasoning/consistency</strong> - Check consistency
        </div>
        
        <h2>Quick Start</h2>
        <p>Create a class:</p>
        <pre><code>curl -X POST http://localhost:5002/api/ontology/classes \\
  -H "Content-Type: application/json" \\
  -d '{"id": "Person", "label": "Person", "description": "A human being"}'</code></pre>
        
        <h2>Documentation</h2>
        <p>See <code>ONTOLOGY_EDITOR_PRODUCT.md</code> for full documentation</p>
    </body>
    </html>
    """


if __name__ == '__main__':
    logger.info("Starting Ontology Editor API server...")
    logger.info("Server running at http://localhost:5002")
    app.run(host='0.0.0.0', port=5002, debug=True)
