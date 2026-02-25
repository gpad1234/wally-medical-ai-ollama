---
layout: default
title: Features
---

# 🎨 Features

WALLY combines ontology graph visualization with an AI-powered medical diagnostic reasoner. Here's a comprehensive overview of all features.

---

## 🔍 Fish-Eye Graph Visualization

The signature feature of WALLY - an intelligent focus+context view that scales nodes based on their distance from the center of attention.

### How It Works

The fish-eye effect applies **distance-based scaling** to create a natural focus:

| Distance | Scale | Visual Effect |
|----------|-------|---------------|
| 0 (Center) | 1.8x | Bold labels, bright glow, 🎯 marker |
| 1 (Near) | 1.3x | Subtle glow, clear labels |
| 2 (Mid) | 1.0x | Normal size, full visibility |
| 3 (Far) | 0.7x | Reduced size, context awareness |
| 4+ (Edge) | 0.5x | Minimal, background context |

### Benefits

- **Focus without losing context** - See detail AND big picture
- **Reduces cognitive load** - Natural hierarchical perception
- **Scales to large graphs** - 1000+ nodes remain navigable
- **Beautiful aesthetics** - Gradients, glows, smooth transitions

---

## 🗺️ Interactive MiniMap

A powerful overview + navigation tool in the bottom-right corner.

### Capabilities

✅ **Click-to-Pan** - Click anywhere to move viewport  
✅ **Drag-to-Navigate** - Drag the viewport rectangle  
✅ **Scroll-to-Zoom** - Zoom in/out with mouse wheel  
✅ **Visual Feedback** - Red center node, blue context nodes  
✅ **Real-time Updates** - Syncs with main view instantly

### Usage Tips

1. Use MiniMap for **quick jumps** to distant graph areas
2. **Drag the viewport rectangle** for precise positioning
3. **Scroll on MiniMap** for alternative zoom control
4. Watch the **red dot** to track your current focus

---

## 🖱️ Click-to-Recenter

Transform any node into the new center of attention with a single click.

### How It Works

1. Click any node in the main view or MiniMap
2. API fetches new viewport centered on that node
3. Graph smoothly updates with new fish-eye effect
4. MiniMap updates to show new position

### Use Cases

- **Explore hierarchies** - Jump from parent to child classes
- **Follow relationships** - Navigate property connections
- **Compare contexts** - Switch between different focal points
- **Discovery mode** - Click-through graph organically

---

## 📊 Viewport-Based Pagination

Smart loading strategy that fetches only what you need to see.

### Algorithm: BFS Fish-Eye

```
1. Start from center node
2. Use BFS to explore neighbors
3. Track distance from center (0, 1, 2, ...)
4. Load nodes within radius limit
5. Apply bidirectional traversal (parent ↔ child)
6. Return nodes with distance metadata
```

### Performance

- **Fast initial load** - ~100ms for 50-node viewport
- **Minimal data transfer** - Only visible nodes fetched
- **Efficient memory** - No need to load entire ontology
- **Scalable** - Constant performance regardless of total graph size

### Configuration

- **Radius slider** (1-5 hops) - Control viewport depth
- **Limit parameter** - Max nodes per viewport (default: 50)
- **Center node** - Current focus point

---

## 🎛️ Interactive Controls

### Radius Slider

Adjust the depth of the fish-eye viewport:

- **Radius 1** - Only direct neighbors (minimal context)
- **Radius 2** - Two hops (balanced view) ⭐ Default
- **Radius 3** - Three hops (broad context)
- **Radius 4-5** - Extended view (maximum awareness)

### Viewport Status

Real-time feedback on current view:

- 📍 **Node count** - Number of visible nodes
- 🔗 **Edge count** - Number of visible connections
- 🎯 **Center** - Current focal node

---

## 🎨 Visual Design System

### Node Styling by Type

**OWL Classes** 🔵
- Gradient: Blue (#3b82f6 → #1d4ed8)  
- Represents: Concepts and categories

**OWL Properties** 🟢
- Gradient: Green (#10b981 → #047857)  
- Represents: Relationships and attributes

**OWL Individuals** 🟡
- Gradient: Amber (#f59e0b → #d97706)  
- Represents: Instances and data

### Glow Effects

- **Center node:** Large glow (30px radius, double layer)
- **Distance 1:** Medium glow (15px radius, single layer)
- **Distance 2+:** No glow (reduces visual clutter)

### Animations

- **Hover:** Subtle scale increase
- **Click:** Pulse effect
- **Loading:** Smooth fade-in
- **Recentering:** Smooth position transitions

---

## 🔗 Edge Rendering

### Connection Types

- **Smooth step edges** - Clean, professional appearance
- **Animated edges** - Optional (disabled by default for performance)
- **Arrow markers** - Directional flow indicators
- **Opacity control** - 60% to reduce visual noise

### Edge Intelligence

- **Bidirectional support** - Handles A→B and B→A
- **Connection handles** - Top (target) and bottom (source)
- **Hidden handles** - Clean node appearance (opacity 0)

---

## 📱 Responsive Layout

### Header Section

- **Title & branding** - "🔍 Fish-Eye Graph View"
- **Status badges** - Node count, edge count, center node
- **Radius control** - Slider with live value display
- **Usage hint** - "💡 Click nodes to recenter | Click/drag MiniMap to navigate"

### Graph Container

- **Full viewport** - Maximizes available space
- **React Flow canvas** - Professional graph rendering
- **Background grid** - Subtle spatial reference
- **Zoom controls** - +/- buttons, fit view, lock/unlock

---

## ⚡ Performance Features

### Optimization Techniques

1. **Memoized node types** - Prevents unnecessary re-renders
2. **Key-based re-mounting** - Forces clean updates on center change
3. **Lazy edge rendering** - Only visible connections drawn
4. **CSS animations** - GPU-accelerated transforms
5. **Fit view caching** - Optimized viewport calculations

### Loading States

- **Spinner animation** - Rotating CSS loader
- **Loading overlay** - Non-blocking UI feedback
- **Error handling** - Clear error messages with retry options

---

## 🛠️ Developer Features

### Debug Console

Extensive logging for development:

```javascript
console.log('🔍 Loading viewport:', { center, radius });
console.log('📦 API Response:', result);
console.log('✅ Viewport data:', { nodes, edges, levels });
console.log('🎨 Created React Flow nodes:', flowNodes.length);
console.log('Sample positions:', flowNodes.slice(0, 3));
```

### Data Structures

**Node Format:**
```javascript
{
  id: "demo:Person",
  label: "Person",
  type: "owl:Class",
  distance_from_center: 1,
  data: { ... },
  metadata: { neighbor_count: 3 }
}
```

**Edge Format:**
```javascript
{
  id: "demo:Person-owl:Thing",
  source: "demo:Person",
  target: "owl:Thing",
  type: "connected"
}
```

---

## 🚀 Coming Soon

Features planned for future releases:

### Week 1 Enhancements
- 🔍 **Search bar** - Find nodes by name or type
- 🎯 **Filters** - Show/hide by node type
- 📊 **Enhanced stats** - Detailed viewport analytics

### Week 2 Polish
- 🎬 **Smooth animations** - Transitions between recenters
- 🖐️ **Hover tooltips** - Full node details on hover
- 🌙 **Dark mode** - Alternative color scheme

### Week 3-4 Scaling
- 💾 **Virtual scrolling** - Handle 1000+ node lists
- 🌊 **Streaming viewport** - Progressive node loading
- ⚡ **Caching layer** - Redis for frequently accessed views
- 📈 **Performance dashboard** - Real-time metrics

---

## 🏥 Medical AI Reasoner

**Version 2.0** — Added February 20, 2026

An AI-powered diagnostic reasoning engine that uses weighted graph traversal over a medical knowledge ontology to perform differential diagnosis.

### How It Works

```
User Input (symptoms)
        │
        ├──── Click Mode: select from symptom panel
        │
        └──── NLP Mode: type free text
                    │
                    ▼
            Llama 3.2 (Ollama)
            POST /llm/extract-symptoms
                    │
                    ▼
            Symptom name → ontology ID mapping
        │
        ▼
Weighted Graph Traversal  O(D × S)
- For each Disease D:
  - For each Symptom S present:
    - score += edge_weight(D, S)
- Normalize to percentage confidence
        │
        ▼
Ranked Diagnoses + Treatment Recommendations
```

### Knowledge Graph

| Entity | Count | Source |
|--------|-------|--------|
| Diseases | 7 | `medical_ontology.ttl` → DO-enriched |
| Symptoms | 20 | `medical_ontology.ttl` with edge weights |
| Treatments | 14 | `medical_ontology.ttl` with type classification |
| Hierarchy nodes | 8 | Respiratory / GI / Neuro / Cardio |
| Edge weights | 0.1 – 0.95 | Symptom specificity per disease |

**Diseases covered:** Common Cold (J00), Influenza (J11.1), Pneumonia, Bronchitis (J20), Gastroenteritis (K52.9), Migraine (G43), Hypertension (I10)

### Input Modes

**Click Mode** — Interactive symptom selection:
1. Open the 🏥 Medical AI Reasoner tab
2. Click symptoms in the panel to toggle them on/off
3. Click "Diagnose" to run the reasoning algorithm instantly

**NLP Mode** — Natural language input via LLM:
1. Click "💬 Describe with AI" toggle
2. Type free text: *"I've had a fever and bad cough for 3 days, feel exhausted"*
3. Click "Extract Symptoms" → Llama 3.2 returns symptom array
4. Symptoms are mapped to ontology IDs and diagnosis runs automatically

### LLM Integration Details

- **Model**: `llama3.2:1b` hosted via Ollama on the same droplet
- **Endpoint**: `POST https://161.35.239.151/llm/extract-symptoms`
- **Response**: `{"symptoms": ["fever", "cough", "fatigue"], "model": "llama3.2:1b"}`
- **Cold start**: ~90s (loads from swap on 1 GB droplet); warm: ~5–15s
- **Cost**: $0 — no API keys, fully self-hosted

---

## � RDF Medical Ontology Backend

**Added February 22, 2026** — The Medical AI Reasoner is now backed by a real RDF/OWL knowledge graph stored in `sample_data/medical_ontology.ttl`, enriched with data from the [Human Disease Ontology](https://disease-ontology.org/) (CC BY 4.0).

### Data Pipeline

```
Disease Ontology API          medical_ontology.ttl
(disease-ontology.org)   →   (RDF/Turtle source          →   Flask /api/ontology/medical   →   React UI
                              of truth)                       (rdflib parser)

scripts/enrich_from_do.py
  - Fetches DOID, definitions,
    ICD-10-CM, MeSH per disease
  - Idempotent: re-run anytime
    to get latest DO releases
```

### Disease Ontology Enrichment

Every disease in the knowledge graph is cross-referenced with the official [Human Disease Ontology](https://disease-ontology.org/):

| Disease | DOID | ICD-10-CM | MeSH | Synonyms |
|---------|------|-----------|------|----------|
| Common Cold | [DOID:10459](https://disease-ontology.org/do#DOID_10459) | J00 | D003139 | acute coryza, acute nasopharyngitis |
| Influenza | [DOID:8469](https://disease-ontology.org/do#DOID_8469) | J11.1 | D007251 | flu |
| Pneumonia | [DOID:552](https://disease-ontology.org/do#DOID_552) | — | D011014 | acute pneumonia |
| Bronchitis | [DOID:6132](https://disease-ontology.org/do#DOID_6132) | J20, J40, J42 | D001991 | chest cold |
| Gastroenteritis | [DOID:2326](https://disease-ontology.org/do#DOID_2326) | K52.9 | D005759 | cholera morbus |
| Migraine | [DOID:6364](https://disease-ontology.org/do#DOID_6364) | G43 | D008881 | migraine disorder |
| Hypertension | [DOID:10763](https://disease-ontology.org/do#DOID_10763) | I10 | D006973 | HTN, hyperpiesia |

### What Appears in the UI

When the Medical AI Reasoner returns a diagnosis, each result card shows:
- 🔵 **DOID badge** — official disease ID, clickable → disease-ontology.org
- 🟢 **ICD-10-CM code** — standard clinical classification
- 💜 **Official definition** — verbatim from the Disease Ontology
- 🟣 **Synonym chips** — alternative names (up to 3)

### Ontology Editor Integration

The same TTL file also powers the **Ontology Editor** graph tab via `GET /api/ontology/medical/graph`:
- **5 OWL classes**: `owl:Thing` → `med:Disease`, `med:Symptom`, `med:Treatment`, `med:HierarchyNode`
- **49 individuals**: all diseases, symptoms, treatments, and hierarchy nodes rendered as graph nodes
- Class hierarchy shown with `subClassOf` arrows in ReactFlow

### Staying Up to Date

The Disease Ontology team publishes regular releases. To pull the latest definitions:

```bash
python3 scripts/enrich_from_do.py
git add sample_data/medical_ontology.ttl
git commit -m "chore: update DO enrichment"
```

The script is idempotent — safe to re-run at any time.

---

## �📖 Feature Guides

Detailed documentation for each feature:

- [Getting Started →](getting-started)
- [Development Guide →](development)
- [Architecture Overview →](architecture)
- [API Reference →](api/)

---

## 🎯 Feature Matrix

| Feature | Status | Version | Notes |
|---------|--------|---------|-------|
| Fish-Eye Visualization | ✅ Live | 1.0 | Core feature |
| Click-to-Recenter | ✅ Live | 1.0 | Main interaction |
| Interactive MiniMap | ✅ Live | 1.1 | Added Feb 19 |
| Radius Control | ✅ Live | 1.0 | 1-5 hops |
| BFS Pagination | ✅ Live | 1.0 | Backend algorithm |
| Bidirectional Traversal | ✅ Live | 1.0 | Full graph navigation |
| Medical AI Reasoner | ✅ Live | 2.0 | Added Feb 20 |
| NLP Symptom Extraction | ✅ Live | 2.0 | Llama 3.2 via Ollama |
| Treatment Recommendations | ✅ Live | 2.0 | Per-diagnosis suggestions |
| RDF TTL Ontology Backend | ✅ Live | 2.1 | Added Feb 22 |
| Disease Ontology (DO) Enrichment | ✅ Live | 2.1 | DOID + ICD-10 + MeSH |
| DOID Badges + ICD-10 in UI | ✅ Live | 2.1 | Clickable DO links |
| Ontology Editor ← Live TTL | ✅ Live | 2.1 | 5 classes, 49 instances |
| Search Bar | 🚧 Planned | 2.2 | Week 1 |
| Node Filters | 🚧 Planned | 2.2 | Week 1 |
| SPARQL Query Interface | 🚧 Planned | 3.0 | Future |
| DO Full Subtree Import | 🚧 Planned | 3.0 | DOID:1579 respiratory branch |
| Dark Mode | 🚧 Planned | 3.0 | Future |

---

[← Back to Home](./) | [Getting Started →](getting-started)
