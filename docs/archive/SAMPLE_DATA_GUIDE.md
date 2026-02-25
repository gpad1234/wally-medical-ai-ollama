# Sample Data Import Guide

## 🎯 Quick Start

Import sample ontology data into the editor:

```bash
# Make sure API is running
lsof -i :5002  # Should show Python process

# Import university domain
source .venv/bin/activate
python3 import_ontology.py sample_data/university_ontology.json

# Import biomedical domain
python3 import_ontology.py sample_data/biomedical_ontology.json
```

## 📦 Available Sample Datasets

### 1. University Domain (`university_ontology.json`)

**Classes:** Person, Student, Professor, Course, Department, Organization  
**Properties:** teaches, enrolledIn, worksFor, hasName, hasEmail, hasGPA  
**Instances:** 2 professors, 2 students, 2 courses, 2 departments  

**Use case:** Academic knowledge graphs, course management, organizational hierarchies

### 2. Biomedical Domain (`biomedical_ontology.json`)

**Classes:** Disease, Symptom, Treatment, Medication, Procedure  
**Properties:** hasSymptom, treatedBy, severity  
**Instances:** Influenza, symptoms (fever, cough), treatments  

**Use case:** Medical knowledge bases, clinical decision support, health informatics

## 🔍 Verify Import

```bash
# Check statistics
curl http://localhost:5002/api/ontology/statistics | python3 -m json.tool

# List all classes  
curl http://localhost:5002/api/ontology/classes | python3 -m json.tool

# View hierarchy
curl http://localhost:5002/api/ontology/hierarchy | python3 -m json.tool

# List instances
curl http://localhost:5002/api/ontology/instances | python3 -m json.tool
```

## 📝 Create Your Own Sample Data

Format:

```json
{
  "name": "My Ontology",
  "description": "Description here",
  "version": "1.0",
  "classes": [
    {
      "id": "MyClass",
      "label": "My Class",
      "description": "A sample class",
      "parent_classes": ["owl:Thing"],
      "is_abstract": false
    }
  ],
  "properties": [
    {
      "id": "myProperty",
      "label": "my property",
      "property_type": "OBJECT",
      "domain": ["MyClass"],
      "range": ["AnotherClass"]
    }
  ],
  "instances": [
    {
      "id": "instance1",
      "label": "Instance 1",
      "class_id": "MyClass",
      "properties": {
        "hasName": "Example"
      }
    }
  ]
}
```

Save as `sample_data/my_ontology.json` and import:

```bash
python3 import_ontology.py sample_data/my_ontology.json
```

## 🔄 Re-import / Update

To reload data (Warning: this adds to existing data, doesn't replace):

```bash
# Clear database first (restart API server)
lsof -ti:5002 | xargs kill -9
sleep 2
source .venv/bin/activate && python3 ontology_api.py &

# Then import fresh data
python3 import_ontology.py sample_data/university_ontology.json
```

## 🛠️ Troubleshooting

**API not running:**
```bash
./start_ontology.sh
# or manually:
source .venv/bin/activate && python3 ontology_api.py
```

**Import errors:**
- Check JSON syntax is valid
- Ensure parent classes exist before children
- Verify property types: "OBJECT", "DATA", or "ANNOTATION"

**View import logs:**
```bash
tail -f logs/ontology_api.log
```

## 🎨 Next Steps After Import

1. **Query the data:**
   ```bash
   curl http://localhost:5002/api/ontology/classes/Person
   curl http://localhost:5002/api/ontology/instances/prof_alice
   ```

2. **Build a frontend** to visualize the hierarchy

3. **Add more data** via API calls

4. **Export** your ontology (feature to be added)

---

**Sample files location:** `sample_data/`  
**Importer script:** `import_ontology.py`  
**API docs:** See `ONTOLOGY_EDITOR_PRODUCT.md`
