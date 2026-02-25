# Node Property Dialog Feature

## Overview
The Node Property Dialog allows users to view and edit node properties directly from the graph visualization UI. Users can access it by either:
1. **Clicking on a node in the diagram** (on the canvas)
2. **Clicking on a node in the sidebar** (in the node list)

## Features

### View Properties
- **Node ID**: Read-only identifier (cannot be changed)
- **Name**: Display name for the node
- **Role**: Role/title of the node (e.g., "manager", "developer")
- **Team**: Team assignment (e.g., "engineering", "design")

### Edit Properties
- All editable fields support real-time input
- Form validation ensures required fields are filled
- Error messages provide clear feedback

### Dialog UI
- **Modal overlay** with semi-transparent background
- **Smooth animations** for open/close transitions
- **Close button** (×) in the header
- **Cancel/Save buttons** in the footer
- **Responsive design** works on mobile and desktop

## Usage

### Opening the Dialog

**From the Graph (Canvas):**
```
Click on any node in the D3.js force-directed graph
```

**From the Sidebar:**
```
Click on any node item in the "Nodes" section of the sidebar
```

### Editing a Node

1. Click to open the dialog
2. Modify the fields:
   - Name (required)
   - Role
   - Team
3. Click "Save Changes" to persist
4. Dialog closes automatically on successful save

### Validation

- **Name field**: Required - cannot be empty
- **Node ID**: Disabled - auto-populated and cannot be changed
- **Role & Team**: Optional fields

## File Structure

```
graph-ui/src/components/NodePropertyDialog/
├── NodePropertyDialog.jsx      # Main component
└── NodePropertyDialog.css      # Styles

graph-ui/src/components/Graph/
└── Graph.jsx                   # Updated to include dialog trigger

graph-ui/src/components/Sidebar/
└── Sidebar.jsx                 # Updated to include dialog trigger
```

## Component API

### NodePropertyDialog

```jsx
<NodePropertyDialog
  node={selectedNode}           // Node object to edit
  isOpen={isOpen}              // Boolean - controls visibility
  onClose={handleClose}        // Callback when dialog closes
/>
```

**Props:**
- `node` (Object): Node data { id, data: { name, role, team } }
- `isOpen` (Boolean): Whether dialog is visible
- `onClose` (Function): Called when user closes dialog

## Styling

The dialog uses a modern, clean design with:
- Gradient header backgrounds
- Smooth transitions and animations
- Color-coded buttons (blue for save, gray for cancel)
- Error states with red borders/text
- Disabled field styling for read-only fields
- Responsive layout for mobile devices

## Integration Points

1. **Graph.jsx**: Triggers dialog on node click
2. **Sidebar.jsx**: Triggers dialog on sidebar node click
3. **graphStore.js**: `updateNode()` method persists changes to backend

## Error Handling

- Displays error messages in red banner
- Validation errors appear inline under fields
- Server errors caught and displayed to user
- Dialog remains open if save fails

## Future Enhancements

Potential improvements:
- Add node color picker
- Add tags/labels for nodes
- Batch edit multiple nodes
- Preview changes in real-time on graph
- Undo/Redo functionality
- Delete node from dialog
