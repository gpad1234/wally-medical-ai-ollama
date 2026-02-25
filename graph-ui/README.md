# Graph UI - React Frontend

A lightweight React + D3.js visualization dashboard for the Graph Database.

## Quick Start

```bash
# Install dependencies (already done)
npm install

# Start development server
npm run dev
```

The app will be available at **http://localhost:5173**

## Features

- **Graph Visualization**: Interactive D3.js force-directed graph
- **Chat Interface**: Natural language queries for graph operations
- **Sidebar Stats**: Real-time graph statistics and node/edge lists
- **Real-time Updates**: All changes reflect immediately

## Architecture

```
src/
├── components/
│   ├── Graph/         # D3.js visualization component
│   ├── Chat/          # Natural language interface
│   └── Sidebar/       # Stats and node/edge lists
├── services/
│   └── api.js         # Axios-based API client
├── store/
│   └── graphStore.js  # Zustand state management
└── App.jsx            # Main layout component
```

## Technology Stack

- **React 18**: UI framework
- **Vite**: Build tool (lightning fast)
- **D3.js**: Graph visualization
- **Zustand**: State management (lightweight)
- **Axios**: HTTP client for API calls

## API Integration

Connects to Flask backend at `http://127.0.0.1:5000`

### Supported Operations

- **Nodes**: Add, update, delete, list
- **Edges**: Add, remove
- **Algorithms**: Shortest path, BFS, DFS, topological sort
- **Search**: Node search with predicates

## Natural Language Examples

```
"add node Alice"
"connect Alice to Bob"
"path from Alice to Bob"
"BFS from Alice"
"list nodes"
"delete node Alice"
```

## Performance

- Ultra-fast HMR with Vite
- Minimal bundle size
- Smooth D3.js animations
- Real-time updates

## Production Build

```bash
npm run build
```

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
