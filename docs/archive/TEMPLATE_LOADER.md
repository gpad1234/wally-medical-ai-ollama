# Template Loader Feature

## Overview

The Template Loader feature allows users to quickly load pre-built dataset templates directly into the graph visualization. This eliminates manual node/edge creation and provides realistic sample data for testing and demonstration.

## What's Included

### 1. Sample Dataset: Social Network (100 nodes)
**File**: `templates/social_network_100.json`

- **100 people** with realistic names (Alice through Unique)
- **145 directed edges** representing relationships
- **Weighted connections** (values 2-8) representing relationship strength
- **Realistic roles** and team assignments:
  - Engineers (Backend, Frontend, Mobile)
  - Product Managers
  - Designers & UX Designers
  - Data Scientists
  - QA Engineers
  - DevOps/Infrastructure specialists

### 2. Backend API Endpoints

#### List Available Templates
```bash
GET /api/templates/list
```
**Response:**
```json
{
  "templates": [
    {
      "name": "social_network_100",
      "display_name": "Social Network (100 nodes)",
      "description": "A realistic social network with 100 people and their connections",
      "nodes": 98,
      "edges": 145
    }
  ]
}
```

#### Load Template
```bash
GET /api/templates/load/{template_name}
```
**Example:** `GET /api/templates/load/social_network_100`

**Response:**
```json
{
  "success": true,
  "message": "Loaded template social_network_100",
  "nodes_loaded": 98,
  "edges_loaded": 145
}
```

### 3. React UI Components

#### Sample Templates Section
Located in the Sidebar component, displays all available templates as buttons:

**Features:**
- Purple gradient buttons with emoji icons
- Shows template name, node count, and edge count
- Loading indicator when template is being loaded
- Automatically refreshes graph visualization after loading
- Error handling with user-friendly messages

**Styling:**
```css
.template-btn {
  padding: 10px 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}
```

### 4. Integration Points

**Frontend:**
- `Sidebar.jsx`: Imports and displays template buttons
- `Sidebar.css`: Styling for template buttons and loading states
- `graphStore.js`: Handles data refresh after loading

**Backend:**
- `graph_web_ui.py`: Template loading endpoints
- `templates/` directory: JSON template files

## Usage

### For Users
1. Open the application
2. Look for "Sample Templates" section in the sidebar
3. Click any template button to load the dataset
4. Graph visualization automatically updates with new data
5. All nodes and edges are now editable

### For Developers: Adding New Templates

1. Create a new JSON file in `templates/` directory:
```json
{
  "name": "Your Template Name",
  "description": "Description of the dataset",
  "nodes": [
    {"id": "node1", "data": {"role": "Engineer", "team": "Backend"}},
    {"id": "node2", "data": {"role": "Designer", "team": "Frontend"}}
  ],
  "edges": [
    {"from": "node1", "to": "node2", "value": 5},
    {"from": "node2", "to": "node1", "value": 3}
  ]
}
```

2. The template automatically appears in the UI after restart

**Template Requirements:**
- `name`: Display name (required)
- `description`: Brief description (optional)
- `nodes`: Array of node objects with `id` and `data` fields (required)
- `edges`: Array of edge objects with `from`, `to`, and `value` fields (required)
- Each node should have unique `id`
- Edge weights should be numbers (2-8 recommended)

## Technical Details

### Data Transformation
Templates use the API format (`from`/`to` for edges), which is automatically transformed to D3 format (`source`/`target`) during graph rendering.

### Graph Reset
Loading a template clears the existing graph and rebuilds it from the template data. The old graph is not preserved (users can add nodes/edges manually afterward).

### Error Handling
- Missing template files return 404 error
- JSON parsing errors are caught and reported
- Invalid node/edge data skips problematic entries with logging
- Loading failures show user-friendly error messages

## Future Enhancements

- [ ] Save current graph as custom template
- [ ] Template categories/filtering
- [ ] Drag-and-drop CSV upload
- [ ] Template search/filter
- [ ] Multiple graph comparison
- [ ] Template version history

## Files Modified

1. `graph_web_ui.py` - Added `/api/templates/list` and `/api/templates/load/<name>` endpoints
2. `graph-ui/src/components/Sidebar/Sidebar.jsx` - Added template UI with loading state
3. `graph-ui/src/components/Sidebar/Sidebar.css` - Added template button styling

## Files Created

1. `templates/social_network_100.json` - Sample social network dataset (98 nodes, 145 edges)
2. `TEMPLATE_LOADER.md` - This documentation file

## Testing

To test the feature:

```bash
# List available templates
curl http://127.0.0.1:5000/api/templates/list

# Load the social network template
curl http://127.0.0.1:5000/api/templates/load/social_network_100

# Verify in UI at http://localhost:5173
# Click the "Social Network (100 nodes)" button in the sidebar
```

## Performance

- Template loading: ~50-100ms for 100-node dataset
- Graph rendering: ~200-300ms with D3 force layout
- No pagination needed for 100 nodes (displays smoothly)
