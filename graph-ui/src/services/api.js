import axios from 'axios';

const API_URL = 'http://127.0.0.1:5001';

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log('🔵 API Request:', config.method.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging and error handling
api.interceptors.response.use(
  (response) => {
    console.log('✅ API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.message, error.config?.url);
    if (error.code === 'ECONNREFUSED') {
      console.error('⚠️  Cannot connect to API. Is Flask running on port 5000?');
    }
    return Promise.reject(error);
  }
);

// Nodes
export const getNodes = () => api.get('/api/graph/nodes');
export const getNode = (id) => api.get(`/api/graph/node/${id}`);
export const addNode = (id, data) => api.post('/api/graph/node', { id, data });
export const updateNode = (id, data) => api.put(`/api/graph/node/${id}`, { data });
export const deleteNode = (id) => api.delete(`/api/graph/node/${id}`);

// Edges
export const addEdge = (from, to, weight = 1) => 
  api.post('/api/graph/edge', { from, to, weight });
export const deleteEdge = (from, to) => 
  api.delete('/api/graph/edge', { data: { from, to } });

// Graph operations
export const getVisualization = () => api.get('/api/graph/visualization');
export const getStats = () => api.get('/api/graph/stats');
export const getNeighbors = (id) => api.get(`/api/graph/neighbors/${id}`);
export const searchNodes = (predicate) => api.post('/api/graph/search', { predicate });
export const shortestPath = (start, target) => 
  api.post('/api/graph/shortest_path', { start, target });
export const bfs = (start) => api.post('/api/graph/bfs', { start });
export const dfs = (start) => api.post('/api/graph/dfs', { start });
export const topologicalSort = () => api.get('/api/graph/topological_sort');

export default api;
