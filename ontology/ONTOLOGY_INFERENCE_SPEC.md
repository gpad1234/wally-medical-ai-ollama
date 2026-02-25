# Ontology Editor: Inference & Reasoning Features
## Technical Specification v1.0

**Date:** February 16, 2026  
**Status:** Phase 1 - In Development  
**Target Release:** rel-2

---

## Executive Summary

This specification outlines the implementation of inference and reasoning capabilities for the Ontology Editor, with property inheritance as the foundational feature. The system will automatically derive knowledge from explicitly defined ontology structures, reducing data redundancy and improving semantic validation.

---

## 1. Overview

### 1.1 Goals
- Implement automatic property inheritance from parent classes to subclasses
- Provide visual indicators distinguishing inherited vs. direct properties
- Validate instances against inherited property requirements
- Establish foundation for advanced reasoning features (transitive relations, type inference)

### 1.2 Success Criteria
- All subclass instances automatically inherit parent class properties
- UI clearly shows inheritance relationships
- Properties marked as required on parent classes are validated on all instances
- System maintains consistent data model with minimal user intervention

### 1.3 Non-Goals (for Phase 1)
- Complex reasoning chains (transitive, inverse properties)
- OWL/RDF full reasoning compliance
- Performance optimization for large ontologies (>10,000 entities)

---

## 2. Phase 1: Property Inheritance with Validation

### 2.1 Core Features

#### 2.1.1 Automatic Property Inheritance
**Behavior:**
- When a class B has parent class A, class B inherits all properties defined on A
- Inheritance is recursive: C inherits from B inherits from A → C gets all properties from A and B
- Inherited properties cannot be removed from subclasses (only overridden with stricter constraints)

**Example:**
```python
# Class Definition
Person (class):
  - name: string (required)
  - age: integer (optional)
  - email: string (required)

Professor (subclass of Person):
  - department: string (required)
  - tenure_status: boolean
  # Automatically inherits: name, age, email

Student (subclass of Person):
  - student_id: string (required)
  - gpa: float
  # Automatically inherits: name, age, email
```

#### 2.1.2 Property Validation
**Required Property Checks:**
- When creating/updating an instance, system validates all required properties (direct + inherited)
- Validation errors show clear inheritance path: "Missing required property 'name' (inherited from Person)"

**Type Validation:**
- Inherited properties maintain their data types
- Values must match expected type (string, integer, float, boolean, reference)

**Validation Timing:**
- On instance creation (POST /api/ontology/instances)
- On instance update (PUT /api/ontology/instances/{id})
- On property definition change (affects all instances)

#### 2.1.3 Visual Indicators

**Class Property View:**
```
Professor (extends Person)
├── Direct Properties
│   ├── ● department: string (required)
│   └── ○ tenure_status: boolean
└── Inherited Properties (from Person)
    ├── ● name: string (required)
    ├── ○ age: integer
    └── ● email: string (required)

Legend:
● Required property
○ Optional property
↓ Inherited property (shown in italics or gray)
```

**Instance Property Editor:**
- Inherited properties displayed in separate collapsible section
- Tooltip shows inheritance source: "Inherited from Person"
- Cannot delete inherited properties, only edit values
- Disabled state for properties that shouldn't be modified

---

## 3. Technical Implementation

### 3.1 Data Model Changes

#### 3.1.1 Enhanced Class Schema
```python
# Current structure (in ontology_api.py)
classes = {
    "class_id": {
        "name": "Professor",
        "parent": "Person",  # Single parent for Phase 1
        "description": "...",
        "properties": ["prop_id_1", "prop_id_2"]  # Direct properties only
    }
}

# Enhanced structure
classes = {
    "class_id": {
        "name": "Professor",
        "parent": "Person",
        "description": "...",
        "direct_properties": ["prop_id_1", "prop_id_2"],
        "inherited_properties": [],  # Computed field, not stored
        "all_properties": []  # Computed: direct + inherited
    }
}
```

#### 3.1.2 Property Metadata
```python
properties = {
    "prop_id": {
        "name": "name",
        "data_type": "string",  # string | integer | float | boolean | reference
        "required": true,
        "default_value": null,
        "defined_on_class": "Person",  # Track original definition
        "description": "Full name of the person"
    }
}
```

### 3.2 Backend API Changes

#### 3.2.1 New Endpoint: Get Class with Inheritance
```http
GET /api/ontology/classes/{class_id}/full
```

**Response:**
```json
{
  "id": "prof_001",
  "name": "Professor",
  "parent": "Person",
  "description": "University professor",
  "direct_properties": [
    {
      "id": "prop_dept",
      "name": "department",
      "data_type": "string",
      "required": true,
      "source": "direct"
    }
  ],
  "inherited_properties": [
    {
      "id": "prop_name",
      "name": "name",
      "data_type": "string",
      "required": true,
      "source": "Person",
      "inheritance_path": ["Person"]
    },
    {
      "id": "prop_age",
      "name": "age",
      "data_type": "integer",
      "required": false,
      "source": "Person",
      "inheritance_path": ["Person"]
    }
  ],
  "all_properties": [/* combined */]
}
```

#### 3.2.2 Modified Endpoint: Create Instance (with validation)
```http
POST /api/ontology/instances
```

**Request:**
```json
{
  "class_id": "prof_001",
  "name": "Dr. Smith",
  "properties": {
    "name": "Alice Smith",
    "age": 45,
    "email": "alice@university.edu",
    "department": "Computer Science",
    "tenure_status": true
  }
}
```

**Validation Logic:**
```python
def validate_instance(class_id, properties):
    """Validate instance against direct + inherited properties"""
    cls = get_class_full(class_id)
    all_required = [p for p in cls['all_properties'] if p['required']]
    
    errors = []
    for prop in all_required:
        if prop['name'] not in properties:
            source = f" (inherited from {prop['source']})" if prop['source'] != 'direct' else ""
            errors.append(f"Missing required property '{prop['name']}'{source}")
    
    # Type validation
    for prop_name, value in properties.items():
        expected_type = get_property_type(prop_name)
        if not validate_type(value, expected_type):
            errors.append(f"Property '{prop_name}' expects {expected_type}, got {type(value)}")
    
    return errors
```

**Error Response (422 Unprocessable Entity):**
```json
{
  "error": "Validation failed",
  "details": [
    "Missing required property 'email' (inherited from Person)",
    "Property 'age' expects integer, got string"
  ]
}
```

#### 3.2.3 New Utility Function: Compute Inheritance Chain
```python
def compute_inherited_properties(class_id, visited=None):
    """Recursively compute all inherited properties"""
    if visited is None:
        visited = set()
    
    if class_id in visited:
        return []  # Prevent circular inheritance
    
    visited.add(class_id)
    cls = classes.get(class_id)
    
    if not cls or not cls.get('parent'):
        return []
    
    parent_id = cls['parent']
    parent_class = classes.get(parent_id)
    
    # Get parent's direct properties
    inherited = []
    for prop_id in parent_class.get('direct_properties', []):
        prop = properties.get(prop_id).copy()
        prop['source'] = parent_class['name']
        prop['inheritance_path'] = [parent_class['name']]
        inherited.append(prop)
    
    # Recursively get parent's inherited properties
    grandparent_props = compute_inherited_properties(parent_id, visited)
    for prop in grandparent_props:
        prop['inheritance_path'].insert(0, parent_class['name'])
        inherited.append(prop)
    
    return inherited
```

### 3.3 Frontend Changes

#### 3.3.1 Class Editor Component
**File:** `ontology-ui/src/components/ClassEditor.jsx` (to be created)

**Features:**
- Split properties into two sections: "Direct" and "Inherited"
- Read-only display of inherited properties
- Visual hierarchy tree showing inheritance chain
- Add/edit buttons only on direct properties

**Component Structure:**
```jsx
<ClassEditor classId={id}>
  <ClassHeader name={cls.name} parent={cls.parent} />
  
  <PropertiesSection title="Direct Properties" editable={true}>
    {cls.direct_properties.map(prop => 
      <PropertyRow key={prop.id} property={prop} editable={true} />
    )}
    <AddPropertyButton />
  </PropertiesSection>
  
  <PropertiesSection title="Inherited Properties" editable={false}>
    {cls.inherited_properties.map(prop => 
      <PropertyRow 
        key={prop.id} 
        property={prop} 
        inherited={true}
        source={prop.source}
        tooltip={`Inherited from ${prop.source}`}
      />
    )}
  </PropertiesSection>
</ClassEditor>
```

#### 3.3.2 Instance Editor Component
**File:** `ontology-ui/src/components/InstanceEditor.jsx` (to be created)

**Features:**
- Display all properties (direct + inherited)
- Show inheritance source in field label
- Validation feedback with inheritance path
- Auto-complete for required fields

**Validation Display:**
```jsx
<Form onSubmit={handleSubmit}>
  {validationErrors.length > 0 && (
    <ValidationPanel errors={validationErrors} />
  )}
  
  {allProperties.map(prop => (
    <FormField
      key={prop.id}
      label={
        <span>
          {prop.name} {prop.required && '*'}
          {prop.source !== 'direct' && (
            <InheritanceTag>
              from {prop.source}
            </InheritanceTag>
          )}
        </span>
      }
      type={prop.data_type}
      required={prop.required}
      value={values[prop.name]}
      onChange={handleChange}
    />
  ))}
</Form>
```

#### 3.3.3 Inheritance Visualization
**Component:** `InheritanceTree.jsx`

**Display Format:**
```
Animal
  ├─ properties: species, habitat
  └─ Mammal
      ├─ properties: warm_blooded (+ inherits: species, habitat)
      └─ Dog
          └─ properties: breed (+ inherits: species, habitat, warm_blooded)
```

**Implementation:**
```jsx
function InheritanceTree({ classId }) {
  const renderNode = (cls, depth = 0) => (
    <div style={{ marginLeft: depth * 20 }}>
      <ClassNode name={cls.name}>
        <PropertiesList 
          direct={cls.direct_properties}
          inherited={cls.inherited_properties}
        />
      </ClassNode>
      {cls.children?.map(child => 
        renderNode(child, depth + 1)
      )}
    </div>
  );
  
  return renderNode(getClassWithChildren(classId));
}
```

---

## 4. Testing Strategy

### 4.1 Unit Tests

**Backend (Python):**
```python
# test_inheritance.py

def test_single_level_inheritance():
    """Test property inheritance from parent to child"""
    person = create_class("Person", properties=[
        {"name": "name", "required": True},
        {"name": "age", "required": False}
    ])
    
    professor = create_class("Professor", parent="Person", properties=[
        {"name": "department", "required": True}
    ])
    
    inherited = compute_inherited_properties(professor.id)
    assert len(inherited) == 2
    assert "name" in [p['name'] for p in inherited]

def test_multi_level_inheritance():
    """Test recursive inheritance through multiple levels"""
    animal = create_class("Animal", properties=[{"name": "species"}])
    mammal = create_class("Mammal", parent="Animal", properties=[{"name": "warm_blooded"}])
    dog = create_class("Dog", parent="Mammal", properties=[{"name": "breed"}])
    
    inherited = compute_inherited_properties(dog.id)
    assert len(inherited) == 2  # species + warm_blooded

def test_instance_validation_with_inheritance():
    """Test instance validation includes inherited required properties"""
    person = create_class("Person", properties=[
        {"name": "name", "required": True}
    ])
    professor = create_class("Professor", parent="Person")
    
    # Should fail: missing required inherited property
    errors = validate_instance(professor.id, {"department": "CS"})
    assert "name" in str(errors)

def test_circular_inheritance_prevention():
    """Test system prevents circular inheritance"""
    a = create_class("A")
    b = create_class("B", parent="A")
    
    # Should fail or return empty
    result = compute_inherited_properties("A", visited={"A", "B"})
    assert result == []
```

**Frontend (Jest + React Testing Library):**
```javascript
// ClassEditor.test.jsx

test('displays inherited properties separately from direct properties', () => {
  const cls = {
    name: 'Professor',
    direct_properties: [{ name: 'department' }],
    inherited_properties: [{ name: 'name', source: 'Person' }]
  };
  
  render(<ClassEditor class={cls} />);
  
  expect(screen.getByText('Direct Properties')).toBeInTheDocument();
  expect(screen.getByText('Inherited Properties')).toBeInTheDocument();
  expect(screen.getByText(/from Person/)).toBeInTheDocument();
});

test('validates required inherited properties on instance creation', async () => {
  const { getByLabelText, getByRole, findByText } = render(
    <InstanceEditor classId="prof_001" />
  );
  
  // Fill only direct property, skip inherited required property
  fireEvent.change(getByLabelText('department'), { target: { value: 'CS' } });
  fireEvent.click(getByRole('button', { name: 'Save' }));
  
  // Should show validation error
  expect(await findByText(/Missing required property 'name'/)).toBeInTheDocument();
});
```

### 4.2 Integration Tests

```python
# test_api_inheritance.py

def test_create_instance_with_inheritance_validation():
    """Test full API flow with inheritance validation"""
    response = client.post('/api/ontology/classes', json={
        "name": "Person",
        "properties": [{"name": "name", "required": True}]
    })
    person_id = response.json()['id']
    
    response = client.post('/api/ontology/classes', json={
        "name": "Professor",
        "parent": person_id,
        "properties": [{"name": "department", "required": True}]
    })
    prof_id = response.json()['id']
    
    # Should fail: missing inherited required property
    response = client.post('/api/ontology/instances', json={
        "class_id": prof_id,
        "name": "Prof. Smith",
        "properties": {"department": "CS"}  # Missing 'name'
    })
    assert response.status_code == 422
    assert "name" in response.json()['details'][0]
```

### 4.3 Manual Test Cases

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| TC-001: View inherited properties | 1. Create parent class with properties<br>2. Create child class<br>3. View child class | Child shows inherited section with parent properties |
| TC-002: Create instance with inheritance | 1. Create class hierarchy<br>2. Create instance of child class<br>3. Fill only direct properties | Validation error shows missing inherited required properties |
| TC-003: Edit inherited property value | 1. Create instance with inherited properties<br>2. Edit inherited property value<br>3. Save | Value updates successfully, property remains in inherited section |
| TC-004: Multi-level inheritance | 1. Create A → B → C class chain<br>2. View class C | Shows properties from both A and B |

---

## 5. Performance Considerations

### 5.1 Caching Strategy
**Problem:** Computing inheritance on every request is expensive for deep hierarchies

**Solution:**
```python
# Add caching layer
from functools import lru_cache

@lru_cache(maxsize=256)
def get_class_full_cached(class_id):
    """Cached version of get_class_full"""
    return compute_class_with_inheritance(class_id)

# Invalidate cache when class structure changes
def on_class_update(class_id):
    get_class_full_cached.cache_clear()
```

### 5.2 Database Optimization
**Current:** In-memory dictionaries (Phase 1 acceptable)  
**Future:** Pre-compute and store inheritance chains in denormalized table

---

## 6. Future Phases (Roadmap)

### Phase 2: Advanced Relationships
- Transitive property chains
- Inverse property auto-generation
- Symmetric/asymmetric relationship handling

### Phase 3: Type Inference
- Domain/Range automatic classification
- "Duck typing" for instances

### Phase 4: Cardinality & Constraints
- Min/max cardinality validation
- Exclusive/disjoint class constraints

### Phase 5: Equivalent Classes & Complex Reasoning
- Class equivalence rules
- SWRL-like rule engine

---

## 7. Implementation Plan

### 7.1 Timeline (2 weeks)

**Week 1: Backend**
- Day 1-2: Data model changes, inheritance computation function
- Day 3-4: API endpoint modifications, validation logic
- Day 5: Unit tests, integration tests

**Week 2: Frontend + Testing**
- Day 6-7: Class editor UI with inheritance display
- Day 8-9: Instance editor with validation
- Day 10: Manual testing, bug fixes, documentation

### 7.2 Deliverables
- [ ] Updated `ontology_api.py` with inheritance logic
- [ ] New `/classes/{id}/full` endpoint
- [ ] Enhanced validation on instance create/update
- [ ] React components: `ClassEditor`, `InstanceEditor`, `InheritanceTree`
- [ ] Test suite: 20+ unit tests, 10+ integration tests
- [ ] Updated `ONTOLOGY_EDITOR_PRODUCT.md` with new features
- [ ] Sample data with multi-level class hierarchy

### 7.3 Dependencies
- No new Python packages required
- Frontend: May need tree visualization library (optional: `react-d3-tree`)

---

## 8. Open Questions

1. **Multiple Inheritance:** Should we support multiple parent classes in future?
   - **Decision:** Phase 1 = single parent only. Revisit in Phase 2.

2. **Property Override:** Can subclass override inherited property constraints?
   - **Decision:** Phase 1 = no override, only stricter constraints allowed.

3. **Inheritance Visualization:** Tree view vs. list view?
   - **Decision:** Start with list, add tree in Phase 2.

---

## 9. Success Metrics

**Phase 1 Completion Criteria:**
- ✅ All unit tests pass (100% coverage on inheritance logic)
- ✅ Manual test cases pass
- ✅ UI clearly shows inherited properties with source
- ✅ Validation catches missing inherited required properties
- ✅ Documentation updated

**User Acceptance:**
- Users can create multi-level class hierarchies
- Instance creation shows clear validation errors
- Inheritance reduces redundant property definitions by >50%

---

## 10. References

- [OntologyEditor.md](OntologyEditor.md) - Current product documentation
- [ontology_api.py](ontology_api.py) - Existing API implementation
- [sample_data/university_ontology.json](sample_data/university_ontology.json) - Sample data structure

---

## Appendix A: Example Data Flow

**Scenario:** Creating a Professor instance

```
1. User Action:
   POST /api/ontology/instances
   {
     "class_id": "prof_001",
     "properties": {
       "department": "Computer Science"
     }
   }

2. Backend Processing:
   a) Load Professor class → has parent Person
   b) Compute inherited properties:
      - name (required) from Person
      - email (required) from Person
      - age (optional) from Person
   c) Validate: FAIL - missing 'name', 'email'
   
3. Response:
   422 Unprocessable Entity
   {
     "error": "Validation failed",
     "details": [
       "Missing required property 'name' (inherited from Person)",
       "Missing required property 'email' (inherited from Person)"
     ]
   }

4. User corrects and resubmits:
   {
     "properties": {
       "name": "Dr. Alice Smith",
       "email": "alice@university.edu",
       "department": "Computer Science"
     }
   }

5. Backend: Validation passes, instance created ✓
```

---

**End of Specification**

*For questions or clarifications, contact the development team.*
