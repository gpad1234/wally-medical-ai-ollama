import { create } from 'zustand';
import * as apiService from '../services/api';

export const useGraphStore = create((set, get) => ({
  // State
  nodes: [],
  edges: [],
  stats: null,
  loading: false,
  error: null,
  selectedNode: null,

  // Actions
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  setSelectedNode: (node) => set({ selectedNode: node }),

  // Data fetching
  fetchVisualization: async () => {
    set({ loading: true, error: null });
    try {
      const response = await apiService.getVisualization();
      let { nodes, edges } = response.data;
      
      // Transform edges from API format (from/to) to D3 format (source/target)
      edges = edges.map(edge => ({
        ...edge,
        source: edge.from,
        target: edge.to
      }));
      
      set({ nodes, edges, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  fetchStats: async () => {
    try {
      const response = await apiService.getStats();
      set({ stats: response.data });
    } catch (error) {
      set({ error: error.message });
    }
  },

  // Node operations
  addNode: async (id, data) => {
    try {
      await apiService.addNode(id, data);
      await get().fetchVisualization();
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },

  updateNode: async (id, data) => {
    try {
      await apiService.updateNode(id, data);
      await get().fetchVisualization();
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },

  deleteNode: async (id) => {
    try {
      await apiService.deleteNode(id);
      await get().fetchVisualization();
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },

  // Edge operations
  addEdge: async (from, to, weight) => {
    try {
      await apiService.addEdge(from, to, weight);
      await get().fetchVisualization();
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },

  deleteEdge: async (from, to) => {
    try {
      await apiService.deleteEdge(from, to);
      await get().fetchVisualization();
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },

  // Graph algorithms
  shortestPath: async (start, target) => {
    try {
      const response = await apiService.shortestPath(start, target);
      return response.data;
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },

  bfs: async (start) => {
    try {
      const response = await apiService.bfs(start);
      return response.data;
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },

  dfs: async (start) => {
    try {
      const response = await apiService.dfs(start);
      return response.data;
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },
}));
