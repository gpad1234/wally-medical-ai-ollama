#!/bin/bash
# Quick view all ontology data

API="http://localhost:5002/api/ontology"

echo "=========================================="
echo "  📊 Ontology Data Quick View"
echo "=========================================="
echo ""

echo "📈 Statistics:"
curl -s $API/statistics | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(f\"  Classes: {d['total_classes' ]}\n  Instances: {d['total_instances']}\n  Properties: {d['total_properties']}\n  Max Depth: {d['max_hierarchy_depth']}\")"

echo ""
echo "📚 Classes:"
curl -s $API/classes | python3 -c "import json,sys; [print(f\"  • {c['label']} ({c['id']})\") for c in json.load(sys.stdin)['data']]"

echo ""
echo "🔍 Full view:"
echo "  python3 view_ontology.py"
echo ""
