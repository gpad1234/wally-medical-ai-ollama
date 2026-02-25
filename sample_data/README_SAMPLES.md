# Sample RDF/OWL Ontologies

This directory contains sample ontology files for testing the RDF/OWL import functionality.

## Available Sample Files

### 1. University Ontology (`university.owl`)
**Format:** OWL/XML (RDF/XML)  
**Domain:** Academic/University  
**Contents:**
- Classes: Person, Student, Professor, Course, Department
- Data Properties: name, email, studentID, courseCode, credits
- Object Properties: teaches, enrolledIn, belongsTo

**Use Case:** Good for testing hierarchical class structures and academic relationships.

### 2. Animal Kingdom Ontology (`animals.ttl`)
**Format:** Turtle (TTL)  
**Domain:** Biology/Zoology  
**Contents:**
- Classes: Animal, Mammal, Bird, Reptile, Fish, Dog, Cat, Habitat
- Data Properties: commonName, scientificName, averageLifespan, canFly, numberOfLegs
- Object Properties: livesIn, preyOf, feeds

**Use Case:** Demonstrates multi-level inheritance and biological classifications.

### 3. Food & Nutrition Ontology (`food.rdf`)
**Format:** RDF/XML  
**Domain:** Food/Nutrition  
**Contents:**
- Classes: Food, Fruit, Vegetable, Meat, Dairy, Dish, Nutrient
- Data Properties: calories, protein, isOrganic, allergen
- Object Properties: contains, hasNutrient

**Use Case:** Shows food hierarchies and nutritional relationships.

## Testing Import

### Via Web UI
1. Start the ontology API server:
   ```bash
   python3 ontology_api.py
   ```

2. Open the React UI at http://localhost:5173

3. Click "📥 Import RDF/OWL" button

4. Select any of the sample files above

### Via API (curl)

Import University ontology:
```bash
curl -X POST http://127.0.0.1:5002/api/ontology/import \
  -F "file=@sample_data/university.owl"
```

Import Animals ontology:
```bash
curl -X POST http://127.0.0.1:5002/api/ontology/import \
  -F "file=@sample_data/animals.ttl"
```

Import Food ontology:
```bash
curl -X POST http://127.0.0.1:5002/api/ontology/import \
  -F "file=@sample_data/food.rdf"
```

### Via Python

```python
import requests

# Import an ontology
with open('sample_data/university.owl', 'rb') as f:
    response = requests.post(
        'http://127.0.0.1:5002/api/ontology/import',
        files={'file': f}
    )
    print(response.json())
```

## Expected Import Results

Each file should import successfully with counts like:

**university.owl:**
- Classes: 5
- Properties: 8
- Instances: 0
- Errors: 0

**animals.ttl:**
- Classes: 9
- Properties: 8
- Instances: 0
- Errors: 0

**food.rdf:**
- Classes: 7
- Properties: 6
- Instances: 0
- Errors: 0

## Formats Supported

The import endpoint supports these RDF serialization formats:
- **OWL/XML** (.owl, .xml, .rdf)
- **Turtle** (.ttl, .turtle)
- **N-Triples** (.nt)
- **Notation3** (.n3)

The format is auto-detected from the file extension.

## Creating Your Own Samples

You can create custom ontologies using tools like:
- [Protégé](https://protege.stanford.edu/) - Desktop ontology editor
- [WebProtégé](https://webprotege.stanford.edu/) - Web-based editor
- Manual editing using the formats above

## Clearing Before Import

To clear the existing ontology before importing a new one:
```bash
curl -X POST "http://127.0.0.1:5002/api/ontology/import?clear=true" \
  -F "file=@sample_data/university.owl"
```
