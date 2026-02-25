# Graph UI - Feature Roadmap & Project Scope

## Project Overview
Building a modern, interactive graph visualization and manipulation platform with:
- **Frontend**: React 19 + Vite + D3.js
- **Backend**: Flask 3.1.2 + Python 3.12
- **Current Status**: MVP complete with core CRUD, visualization, and NLP chat

This document outlines the next iteration of features to build a production-ready system.

---

## Phase 1: Extended Property Management (Next Sprint)
*Complete CRUD capabilities for all graph elements*

### 1.1 Edge Property Dialog
**Priority**: 🔴 HIGH | **Effort**: 🕐 2-3 days | **Dependencies**: None

**User Story**: As a user, I want to click on edges to edit their properties (weight, direction, style)

**Features**:
- Modal dialog triggered by clicking edges in diagram
- Editable fields:
  - Source node (read-only display)
  - Target node (read-only display)
  - Weight/value (numeric input, >0)
  - Direction type (directional, bidirectional, undirected)
  - Custom properties (expandable key-value store)
- Delete edge button with confirmation
- Form validation with inline error messages
- Real-time preview of changes on diagram

**Technical Tasks**:
- [ ] Create `EdgePropertyDialog.jsx` component
- [ ] Create `EdgePropertyDialog.css` with modal styling
- [ ] Add edge click handler in `Graph.jsx`
- [ ] Backend: Add `PUT /api/graph/edge/{from}/{to}` endpoint
- [ ] Backend: Add `DELETE /api/graph/edge/{from}/{to}` endpoint
- [ ] Integration tests for edge modification

**Acceptance Criteria**:
- [ ] Click any edge → dialog opens with current values
- [ ] Edit weight → updates visually, persists to backend
- [ ] Delete edge → confirmation, removed from graph
- [ ] Invalid weight shows error (must be positive)
- [ ] Can add/edit custom properties

**Estimated Story Points**: 5

---

### 1.2 Bulk Operations
**Priority**: 🟡 MEDIUM | **Effort**: 🕐 3-4 days | **Dependencies**: 1.1

**User Story**: As a user, I want to select multiple nodes and perform operations on them (bulk edit, delete)

**Features**:
- Multi-select nodes (Ctrl+click or checkbox mode toggle)
- Visual highlight for selected nodes
- Bulk operations menu:
  - Bulk edit (role, team, name prefix)
  - Bulk delete with confirmation
  - Count indicator ("3 nodes selected")
- Undo support for bulk operations

**Technical Tasks**:
- [ ] Add multi-select state to `graphStore.js`
- [ ] Create `BulkSelectMode.jsx` component for controls
- [ ] Update `Sidebar.jsx` with selection checkboxes
- [ ] Update `Graph.jsx` with visual highlighting
- [ ] Backend: Add `POST /api/graph/bulk_update` endpoint
- [ ] Backend: Add `POST /api/graph/bulk_delete` endpoint

**Acceptance Criteria**:
- [ ] Hold Ctrl and click multiple nodes → all highlight
- [ ] Checkbox mode toggles with button
- [ ] Bulk edit modal shows all selected nodes
- [ ] Changes applied to all selected in one operation
- [ ] Bulk delete shows confirmation with count

**Estimated Story Points**: 8

---

## Phase 2: Search, Discovery & Analytics
*Help users navigate and understand graphs*

### 2.1 Node Search & Advanced Filtering
**Priority**: 🔴 HIGH | **Effort**: 🕐 1-2 days | **Dependencies**: None

**User Story**: As a user, I want to search and filter nodes by multiple criteria to find what I need

**Features**:
- Real-time search box in sidebar
- Multi-criteria filtering:
  - Text search (name, ID, role)
  - Filter by role (dropdown with autocomplete)
  - Filter by team (dropdown with autocomplete)
  - Connected to node (find neighbors)
- Results counter ("5 of 12 nodes")
- Clear filter button
- Highlight matching nodes in diagram

**Technical Tasks**:
- [ ] Create `SearchFilter.jsx` component
- [ ] Add search state to `graphStore.js`
- [ ] Update `Sidebar.jsx` to integrate search
- [ ] Update `Graph.jsx` to highlight matches
- [ ] Add search methods to store (fuzzy matching)

**Acceptance Criteria**:
- [ ] Type "ali" → shows nodes with "ali" in name
- [ ] Matching nodes highlight in diagram
- [ ] Filter dropdowns update dynamically
- [ ] Clear button resets all filters
- [ ] Shows "5 of 12 nodes" counter

**Estimated Story Points**: 5

---

### 2.2 Graph Statistics Dashboard
**Priority**: 🟡 MEDIUM | **Effort**: 🕐 2 days | **Dependencies**: None

**User Story**: As an analyst, I want to see key statistics about my graph structure and node importance

**Features**:
- Enhanced sidebar stats panel:
  - Node degree distribution (histogram)
  - Most connected nodes (top 5 with badges)
  - Isolated nodes (list)
  - Network diameter
  - Average path length
  - Network density percentage
- Auto-update on graph changes
- Optional: small chart visualizations

**Technical Tasks**:
- [ ] Create `StatsDashboard.jsx` component
- [ ] Backend: Add `POST /api/graph/compute_stats` endpoint
- [ ] Add statistics caching to avoid recomputation
- [ ] Use lightweight charting library (e.g., Chart.js)

**Acceptance Criteria**:
- [ ] Stats update within 1 second of graph change
- [ ] Identifies all isolated nodes correctly
- [ ] Degree distribution chart displays properly
- [ ] Shows top 5 most connected nodes

**Estimated Story Points**: 5

---

## Phase 3: Graph Algorithms & Intelligence
*Compute insights and enable advanced queries*

### 3.1 Enhanced Algorithm Suite
**Priority**: 🔴 HIGH | **Effort**: 🕐 4-5 days | **Dependencies**: None

**User Story**: As an analyst, I want to run graph algorithms to discover structure, centrality, and communities

**Algorithms to Implement**:
- Connected Components (find clusters)
- Minimum Spanning Tree (MST)
- Strongly Connected Components (for directed graphs)
- Betweenness Centrality (node importance)
- PageRank (network ranking)
- Community Detection (Louvain algorithm)

**Features**:
- Algorithm selection dropdown
- "Run Algorithm" button with progress indicator
- Results visualization:
  - Highlight affected nodes/edges
  - Color by metric (heat map)
  - Sidebar panel with ranked results
- Result caching (don't recompute if graph unchanged)

**Technical Tasks**:
- [ ] Create `AlgorithmPanel.jsx` component
- [ ] Backend: Implement algorithms in `graph_lib.py`
- [ ] Backend: Add 6 new endpoints (`/api/graph/{algorithm}`)
- [ ] Add result visualization layer to `Graph.jsx`
- [ ] Add loading state and error handling

**Acceptance Criteria**:
- [ ] Select algorithm → runs in <2 seconds for 100 nodes
- [ ] Results display with proper coloring
- [ ] Sidebar shows ranked list
- [ ] Can run different algorithms sequentially
- [ ] Results clear on graph modification

**Estimated Story Points**: 13

---

### 3.2 Path Finding & Visualization
**Priority**: 🟡 MEDIUM | **Effort**: 🕐 2-3 days | **Dependencies**: 3.1

**User Story**: As a user, I want to find and compare all paths between two nodes

**Features**:
- Start/end node selectors
- Find all paths (with depth limit)
- Sort results by:
  - Path length
  - Total weight
  - Feasibility
- Click to highlight selected path
- Show path details (nodes in order, total cost)
- Save/bookmark favorite paths

**Technical Tasks**:
- [ ] Create `PathFinder.jsx` component
- [ ] Backend: Add `POST /api/graph/all_paths` endpoint
- [ ] Backend: Implement DFS/BFS path enumeration
- [ ] Add bookmarks to `graphStore.js`

**Acceptance Criteria**:
- [ ] Find all paths shows all possible routes
- [ ] Results sorted correctly by selection
- [ ] Highlight path animation smooth
- [ ] Works with 100+ nodes

**Estimated Story Points**: 8

---

## Phase 4: Data Persistence & Sharing
*Import, export, and manage graph data*

### 4.1 Import/Export Functionality
**Priority**: 🔴 HIGH | **Effort**: 🕐 2-3 days | **Dependencies**: None

**User Story**: As a user, I want to save and load graph data in multiple formats

**Formats**:
- JSON (native, complete)
- CSV (nodes and edges as separate tables)
- GraphML (standard XML format)
- Graphviz DOT (for documentation)

**Features**:
- Export dialog with format selector
- Download file button
- Import dialog with file picker
- Preview before importing
- Merge or replace current graph options
- Handle large files (1000+ nodes)

**Technical Tasks**:
- [ ] Create `ImportExportDialog.jsx` component
- [ ] Backend: Add `POST /api/graph/export/{format}` endpoint
- [ ] Backend: Add `POST /api/graph/import` endpoint (with format detection)
- [ ] Add format converters for each type
- [ ] File size validation

**Acceptance Criteria**:
- [ ] Export JSON downloads correctly
- [ ] CSV imports with proper node/edge parsing
- [ ] Preview shows structure before import
- [ ] Large files (500 nodes) handle smoothly
- [ ] All metadata preserved in JSON export

**Estimated Story Points**: 8

---

### 4.2 Graph Templates & Presets
**Priority**: 🟡 MEDIUM | **Effort**: 🕐 2 days | **Dependencies**: 4.1

**User Story**: As a new user, I want to load sample graphs to learn and experiment

**Templates**:
- Social Network (realistic people connections)
- Organization Hierarchy (corporate structure)
- Transportation Network (cities and routes)
- Citation Network (academic papers)
- Collaboration Graph (co-authors)

**Features**:
- Template gallery/browser
- One-click load
- Load or merge option
- Custom templates (save current graph as template)

**Technical Tasks**:
- [ ] Create template JSON files
- [ ] Create `TemplateGallery.jsx` component
- [ ] Backend: `/api/graph/templates` endpoint
- [ ] Backend: `/api/graph/load_template/{name}` endpoint

**Acceptance Criteria**:
- [ ] Template gallery shows 5+ templates
- [ ] Load template works smoothly
- [ ] Can save custom as template
- [ ] Templates preview before loading

**Estimated Story Points**: 5

---

## Phase 5: User Experience Polish
*Enhance usability and workflow efficiency*

### 5.1 Keyboard Shortcuts & Command Palette
**Priority**: 🟡 MEDIUM | **Effort**: 🕐 1-2 days | **Dependencies**: None

**Shortcuts**:
```
Ctrl+F   - Focus search box
Ctrl+Z   - Undo
Ctrl+Y   - Redo
Ctrl+A   - Select all nodes
Delete   - Delete selected
Esc      - Deselect / Close dialog
+/-      - Zoom in/out
Space    - Pan mode (drag to move)
Ctrl+K   - Command palette
? or H   - Help/shortcuts
```

**Features**:
- Global keyboard listener
- Command palette (Ctrl+K) for discoverability
- Help modal with shortcuts list
- No conflicts with browser shortcuts

**Technical Tasks**:
- [ ] Create `useKeyboardShortcuts.js` hook
- [ ] Create `CommandPalette.jsx` component
- [ ] Integrate into `App.jsx`
- [ ] Add to global event handlers

**Acceptance Criteria**:
- [ ] All shortcuts functional
- [ ] Help modal lists all shortcuts
- [ ] No console errors on shortcuts
- [ ] Works with browser dev tools open

**Estimated Story Points**: 5

---

### 5.2 Undo/Redo System
**Priority**: 🔴 HIGH | **Effort**: 🕐 3-4 days | **Dependencies**: None

**User Story**: As a user, I want to undo and redo my actions to fix mistakes

**Features**:
- Action history stack (max 100 actions)
- Support all mutations:
  - Add/delete node
  - Edit node properties
  - Add/delete edge
  - Edit edge properties
  - Bulk operations
- Undo/redo buttons in header (with keyboard)
- History cleared on new graph load
- Visual indicator of undo/redo availability

**Technical Tasks**:
- [ ] Create `useHistory.js` hook
- [ ] Refactor all mutations to track actions
- [ ] Update `graphStore.js` for history
- [ ] Add undo/redo buttons to header
- [ ] Persist history in memory (not localStorage)

**Acceptance Criteria**:
- [ ] Undo button reverses last action
- [ ] Redo works after undo
- [ ] Buttons disabled when no history
- [ ] Works with all operation types
- [ ] History clears on new graph

**Estimated Story Points**: 8

---

### 5.3 Enhanced Chat Interface
**Priority**: 🟡 MEDIUM | **Effort**: 🕐 2-3 days | **Dependencies**: 1.1, 1.2

**User Story**: As a user, I want to manipulate the graph using natural language commands

**Enhancements**:
- Command autocomplete dropdown
- Command history (up/down arrows)
- More natural language patterns:
  - "Show me the shortest path from X to Y"
  - "Who has the most connections?"
  - "Delete all nodes with role developer"
  - "Create nodes A, B, C and connect them"
  - "Find communities in this graph"
- Help panel with example queries
- Syntax highlighting in chat

**Technical Tasks**:
- [ ] Enhance NLP parser in `Chat.jsx`
- [ ] Create `ChatHelp.jsx` component
- [ ] Add command history to store
- [ ] Expand backend NLP patterns
- [ ] Add regex/pattern matching for new formats

**Acceptance Criteria**:
- [ ] Chat shows autocomplete suggestions
- [ ] Natural language commands understood
- [ ] Help shows 10+ example commands
- [ ] Command history navigable
- [ ] No console errors on invalid input

**Estimated Story Points**: 8

---

## Phase 6: Production Readiness
*Performance optimization and deployment*

### 6.1 Performance Optimization
**Priority**: 🔴 HIGH | **Effort**: 🕐 2-3 days | **Dependencies**: None

**Areas**:
- Virtualize large node lists (1000+ nodes)
- Optimize D3 rendering with quadtree collision detection
- Lazy-load edges
- Debounce expensive operations
- Memoize expensive computations
- Memory leak detection

**Technical Tasks**:
- [ ] Profile app with 500+ nodes
- [ ] Implement virtualization for sidebar lists
- [ ] Optimize D3 tick function
- [ ] Add React.memo to components
- [ ] Use useMemo/useCallback hooks
- [ ] Test with large graphs

**Acceptance Criteria**:
- [ ] Smooth interaction with 500 nodes
- [ ] No lag with 1000 nodes
- [ ] Search responds in <100ms
- [ ] Lighthouse score > 85

**Estimated Story Points**: 8

---

### 6.2 Docker & Deployment
**Priority**: 🔴 HIGH | **Effort**: 🕐 2-3 days | **Dependencies**: All

**Deployment Stack**:
- Docker containers for Flask and React
- Docker Compose for local development
- GitHub Actions CI/CD pipeline
- Environment configuration (.env)
- Security: CORS, rate limiting, validation

**Technical Tasks**:
- [ ] Create `Dockerfile` for Flask
- [ ] Create `Dockerfile` for React (multi-stage)
- [ ] Create `docker-compose.yml`
- [ ] Add GitHub Actions workflow
- [ ] Add production nginx config
- [ ] Environment variable management

**Acceptance Criteria**:
- [ ] App runs locally with `docker-compose up`
- [ ] Deployable to cloud (AWS/Heroku)
- [ ] CI/CD pipeline builds on push
- [ ] No hardcoded secrets

**Estimated Story Points**: 8

---

### 6.3 Testing & Documentation
**Priority**: 🟡 MEDIUM | **Effort**: 🕐 3-4 days | **Dependencies**: All

**Coverage**:
- Unit tests (React components, utils)
- Integration tests (API calls)
- E2E tests (critical workflows)
- Backend tests (algorithms, API)
- Performance tests

**Documentation**:
- API documentation (Swagger/OpenAPI)
- Component storybook
- User guide / Tutorial
- Developer setup guide

**Technical Tasks**:
- [ ] Set up Jest + React Testing Library
- [ ] Set up Cypress for E2E
- [ ] Create 50+ unit tests
- [ ] Create 10+ E2E test scenarios
- [ ] Generate API docs with Swagger
- [ ] Write comprehensive README

**Acceptance Criteria**:
- [ ] 80%+ code coverage
- [ ] All critical flows tested
- [ ] API docs auto-generated
- [ ] Deployment docs complete

**Estimated Story Points**: 13

---

## Implementation Timeline

```
Phase 1 (Extended CRUD)           - Week 1-2   (13 pts)
  ├─ Edge Dialog + Bulk Ops
  
Phase 2 (Search & Analytics)       - Week 3     (10 pts)
  ├─ Search + Stats Dashboard
  
Phase 3 (Algorithms)               - Week 4-6   (21 pts)
  ├─ Algorithm Suite + Path Finder
  
Phase 4 (Data Persistence)         - Week 7-8   (13 pts)
  ├─ Import/Export + Templates
  
Phase 5 (Polish)                   - Week 9-10  (21 pts)
  ├─ Shortcuts, Undo/Redo, Chat
  
Phase 6 (Production)               - Week 11-13 (29 pts)
  ├─ Performance, Docker, Tests
  
Total Effort: 107 story points ≈ 12-16 weeks (1 dev)
```

---

## Success Metrics

By completion of all phases:

- [ ] ✅ Core features fully implemented (Phases 1-3)
- [ ] ✅ Smooth handling of 1000+ nodes
- [ ] ✅ <100ms response for all operations
- [ ] ✅ 80%+ test coverage
- [ ] ✅ Users can import/export/share graphs
- [ ] ✅ Deployable to production with 1 command
- [ ] ✅ Full API and user documentation
- [ ] ✅ Zero critical bugs

---

## Next Steps

**Recommended Approach**:
1. ✅ Start with **Phase 1** (CRUD completeness)
   - Gives users full control of all graph elements
   - High impact, medium effort
   
2. Then **Phase 2** (UX improvements)
   - Makes existing features more discoverable
   - Quick wins
   
3. Then **Phase 3** (Intelligence)
   - Differentiator from other tools
   - Requires more backend work
   
4. Then **Phases 4-5** (Polish)
   - Data persistence (critical for real use)
   - Workflow efficiency
   
5. Finally **Phase 6** (Deploy)
   - Production readiness
   - CI/CD automation

**Question for you**: Which phase would you like to start with?

