"""
Graph Database with Traversal Algorithms

Supports:
- Import/export from structured text (JSON, adjacency list)
- In-memory storage using SimpleDB
- Graph traversal (BFS, DFS)
- Node/edge operations (add, delete, search)
- Multiple graph types (directed, undirected, weighted)
"""

import json
from typing import List, Dict, Set, Optional, Tuple, Any
from collections import deque
from src.adapters.simple_db import SimpleDB


class GraphDB:
    """Graph database with traversal algorithms"""
    
    def __init__(self, directed: bool = True, weighted: bool = False):
        """
        Initialize graph database
        
        Args:
            directed: True for directed graph, False for undirected
            weighted: True if edges have weights
        """
        self.db = SimpleDB()
        self.directed = directed
        self.weighted = weighted
        
        # Store metadata
        self.db.set("__meta__:directed", str(directed))
        self.db.set("__meta__:weighted", str(weighted))
        self.db.set("__meta__:node_count", "0")
        self.db.set("__meta__:edge_count", "0")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.clear()
        return False
    
    # ========================================================================
    # Node Operations
    # ========================================================================
    
    def add_node(self, node_id: str, data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Add a node to the graph
        
        Args:
            node_id: Unique identifier for the node
            data: Optional dictionary of node attributes
            
        Returns:
            True if node was added, False if already exists
        """
        key = f"node:{node_id}"
        
        if self.db.exists(key):
            return False
        
        # Store node data
        node_data = data or {}
        self.db.set(key, json.dumps(node_data))
        
        # Initialize empty adjacency list
        self.db.set(f"adj:{node_id}", "[]")
        
        # Update node count
        count = int(self.db.get("__meta__:node_count") or "0")
        self.db.set("__meta__:node_count", str(count + 1))
        
        return True
    
    def delete_node(self, node_id: str) -> bool:
        """
        Delete a node and all its edges
        
        Args:
            node_id: Node to delete
            
        Returns:
            True if deleted, False if node doesn't exist
        """
        key = f"node:{node_id}"
        
        if not self.db.exists(key):
            return False
        
        # Remove all edges to/from this node
        edges_to_remove = []
        for edge_key in self.db.keys():
            if edge_key.startswith("edge:"):
                parts = edge_key.split(":")
                if len(parts) >= 3:
                    from_node, to_node = parts[1], parts[2]
                    if from_node == node_id or to_node == node_id:
                        edges_to_remove.append(edge_key)
        
        for edge_key in edges_to_remove:
            self.db.delete(edge_key)
        
        # Remove from adjacency lists
        for adj_key in self.db.keys():
            if adj_key.startswith("adj:") and adj_key != f"adj:{node_id}":
                adj_list = json.loads(self.db.get(adj_key))
                adj_list = [item for item in adj_list if item.get('to') != node_id]
                self.db.set(adj_key, json.dumps(adj_list))
        
        # Delete node data and adjacency list
        self.db.delete(key)
        self.db.delete(f"adj:{node_id}")
        
        # Update node count
        count = int(self.db.get("__meta__:node_count") or "0")
        self.db.set("__meta__:node_count", str(max(0, count - 1)))
        
        return True
    
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Get node data
        
        Args:
            node_id: Node identifier
            
        Returns:
            Dictionary of node attributes including 'id', or None if not found
        """
        key = f"node:{node_id}"
        data = self.db.get(key)
        
        if data:
            node_data = json.loads(data)
            # Include the node ID in the returned dict
            return {
                'id': node_id,
                'data': node_data
            }
        return None
    
    def update_node(self, node_id: str, data: Dict[str, Any]) -> bool:
        """
        Update node data
        
        Args:
            node_id: Node identifier
            data: New node attributes
            
        Returns:
            True if updated, False if node doesn't exist
        """
        key = f"node:{node_id}"
        
        if not self.db.exists(key):
            return False
        
        self.db.set(key, json.dumps(data))
        return True
    
    def node_exists(self, node_id: str) -> bool:
        """Check if node exists"""
        return self.db.exists(f"node:{node_id}")
    
    def get_all_nodes(self) -> List[str]:
        """Get list of all node IDs"""
        nodes = []
        for key in self.db.keys():
            if key.startswith("node:"):
                node_id = key[5:]  # Remove "node:" prefix
                nodes.append(node_id)
        return sorted(nodes)
    
    # ========================================================================
    # Edge Operations
    # ========================================================================
    
    def add_edge(self, from_node: str, to_node: str, weight: float = 1.0, label: str = "") -> bool:
        """
        Add an edge between two nodes
        
        Args:
            from_node: Source node
            to_node: Destination node
            weight: Edge weight (for weighted graphs)
            label: Optional edge label/type
            
        Returns:
            True if edge was added, False otherwise
        """
        # Ensure both nodes exist
        if not self.node_exists(from_node) or not self.node_exists(to_node):
            return False
        
        # Add edge
        edge_key = f"edge:{from_node}:{to_node}"
        edge_data = {}
        if self.weighted:
            edge_data["weight"] = weight
        if label:
            edge_data["label"] = label
        self.db.set(edge_key, json.dumps(edge_data))
        
        # Update adjacency list for from_node
        adj_list = json.loads(self.db.get(f"adj:{from_node}") or "[]")
        edge_info = {"to": to_node}
        if self.weighted:
            edge_info["weight"] = weight
        
        # Remove existing edge to same node (if updating)
        adj_list = [e for e in adj_list if e.get('to') != to_node]
        adj_list.append(edge_info)
        self.db.set(f"adj:{from_node}", json.dumps(adj_list))
        
        # For undirected graphs, add reverse edge
        if not self.directed:
            reverse_edge_key = f"edge:{to_node}:{from_node}"
            self.db.set(reverse_edge_key, json.dumps(edge_data))
            
            adj_list_reverse = json.loads(self.db.get(f"adj:{to_node}") or "[]")
            reverse_edge_info = {"to": from_node}
            if self.weighted:
                reverse_edge_info["weight"] = weight
            
            adj_list_reverse = [e for e in adj_list_reverse if e.get('to') != from_node]
            adj_list_reverse.append(reverse_edge_info)
            self.db.set(f"adj:{to_node}", json.dumps(adj_list_reverse))
        
        # Update edge count
        count = int(self.db.get("__meta__:edge_count") or "0")
        self.db.set("__meta__:edge_count", str(count + 1))
        
        return True
    
    def delete_edge(self, from_node: str, to_node: str) -> bool:
        """
        Delete an edge
        
        Args:
            from_node: Source node
            to_node: Destination node
            
        Returns:
            True if deleted, False if edge doesn't exist
        """
        edge_key = f"edge:{from_node}:{to_node}"
        
        if not self.db.exists(edge_key):
            return False
        
        # Delete edge
        self.db.delete(edge_key)
        
        # Update adjacency list
        adj_list = json.loads(self.db.get(f"adj:{from_node}") or "[]")
        adj_list = [e for e in adj_list if e.get('to') != to_node]
        self.db.set(f"adj:{from_node}", json.dumps(adj_list))
        
        # For undirected graphs, delete reverse edge
        if not self.directed:
            reverse_edge_key = f"edge:{to_node}:{from_node}"
            self.db.delete(reverse_edge_key)
            
            adj_list_reverse = json.loads(self.db.get(f"adj:{to_node}") or "[]")
            adj_list_reverse = [e for e in adj_list_reverse if e.get('to') != from_node]
            self.db.set(f"adj:{to_node}", json.dumps(adj_list_reverse))
        
        # Update edge count
        count = int(self.db.get("__meta__:edge_count") or "0")
        self.db.set("__meta__:edge_count", str(max(0, count - 1)))
        
        return True
    
    def get_edge(self, from_node: str, to_node: str) -> Optional[Dict[str, Any]]:
        """Get edge data"""
        edge_key = f"edge:{from_node}:{to_node}"
        data = self.db.get(edge_key)
        
        if data:
            return json.loads(data)
        return None
    
    def edge_exists(self, from_node: str, to_node: str) -> bool:
        """Check if edge exists"""
        return self.db.exists(f"edge:{from_node}:{to_node}")
    
    def get_neighbors(self, node_id: str) -> List[Dict[str, Any]]:
        """
        Get all neighbors of a node
        
        Returns:
            List of dictionaries with 'to' and optionally 'weight'
        """
        adj_list = self.db.get(f"adj:{node_id}")
        if adj_list:
            return json.loads(adj_list)
        return []
    
    def get_all_edges(self) -> List[Tuple[str, str, Optional[float]]]:
        """
        Get all edges in the graph
        
        Returns:
            List of tuples (from_node, to_node, weight)
        """
        edges = []
        seen = set()
        
        for key in self.db.keys():
            if key.startswith("edge:"):
                parts = key.split(":")
                if len(parts) >= 3:
                    from_node, to_node = parts[1], parts[2]
                    
                    # For undirected graphs, avoid duplicates
                    if not self.directed:
                        edge_tuple = tuple(sorted([from_node, to_node]))
                        if edge_tuple in seen:
                            continue
                        seen.add(edge_tuple)
                    
                    edge_data = json.loads(self.db.get(key))
                    weight = edge_data.get("weight") if self.weighted else None
                    edges.append((from_node, to_node, weight))
        
        return edges
    
    # ========================================================================
    # Graph Traversal Algorithms
    # ========================================================================
    
    def bfs(self, start_node: str, target_node: Optional[str] = None) -> Dict[str, Any]:
        """
        Breadth-First Search traversal
        
        Args:
            start_node: Starting node
            target_node: Optional target node (stops when found)
            
        Returns:
            Dictionary with:
            - 'visited': List of nodes in BFS order
            - 'found': True if target found (if specified)
            - 'path': Path to target (if found)
            - 'distances': Distance from start to each node
        """
        if not self.node_exists(start_node):
            return {"visited": [], "found": False, "path": [], "distances": {}}
        
        visited = []
        queue = deque([start_node])
        visited_set = {start_node}
        parent = {start_node: None}
        distances = {start_node: 0}
        
        while queue:
            current = queue.popleft()
            visited.append(current)
            
            # Check if we found the target
            if target_node and current == target_node:
                path = self._reconstruct_path(parent, start_node, target_node)
                return {
                    "visited": visited,
                    "found": True,
                    "path": path,
                    "distances": distances
                }
            
            # Visit neighbors
            neighbors = self.get_neighbors(current)
            for neighbor_info in neighbors:
                neighbor = neighbor_info['to']
                
                if neighbor not in visited_set:
                    visited_set.add(neighbor)
                    queue.append(neighbor)
                    parent[neighbor] = current
                    distances[neighbor] = distances[current] + 1
        
        # Build path if target was specified
        path = []
        if target_node and target_node in parent:
            path = self._reconstruct_path(parent, start_node, target_node)
        
        return {
            "visited": visited,
            "found": target_node in visited_set if target_node else True,
            "path": path,
            "distances": distances
        }
    
    def dfs(self, start_node: str, target_node: Optional[str] = None) -> Dict[str, Any]:
        """
        Depth-First Search traversal
        
        Args:
            start_node: Starting node
            target_node: Optional target node (stops when found)
            
        Returns:
            Dictionary with:
            - 'visited': List of nodes in DFS order
            - 'found': True if target found (if specified)
            - 'path': Path to target (if found)
        """
        if not self.node_exists(start_node):
            return {"visited": [], "found": False, "path": []}
        
        visited = []
        visited_set = set()
        parent = {}
        
        def dfs_recursive(node):
            visited.append(node)
            visited_set.add(node)
            
            # Check if we found the target
            if target_node and node == target_node:
                return True
            
            # Visit neighbors
            neighbors = self.get_neighbors(node)
            for neighbor_info in neighbors:
                neighbor = neighbor_info['to']
                
                if neighbor not in visited_set:
                    parent[neighbor] = node
                    if dfs_recursive(neighbor):
                        return True
            
            return False
        
        found = dfs_recursive(start_node)
        parent[start_node] = None
        
        # Build path if target was specified
        path = []
        if target_node and target_node in parent:
            path = self._reconstruct_path(parent, start_node, target_node)
        
        return {
            "visited": visited,
            "found": found if target_node else True,
            "path": path
        }
    
    def _reconstruct_path(self, parent: Dict[str, Optional[str]], 
                         start: str, end: str) -> List[str]:
        """Reconstruct path from parent dictionary"""
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = parent.get(current)
        
        path.reverse()
        
        # Verify path starts at start node
        if path and path[0] == start:
            return path
        return []
    
    def find_all_paths(self, start_node: str, end_node: str, 
                      max_length: Optional[int] = None) -> List[List[str]]:
        """
        Find all paths between two nodes
        
        Args:
            start_node: Starting node
            end_node: Ending node
            max_length: Maximum path length (None for unlimited)
            
        Returns:
            List of paths (each path is a list of nodes)
        """
        all_paths = []
        
        def dfs_paths(current, target, path, visited):
            if max_length and len(path) > max_length:
                return
            
            if current == target:
                all_paths.append(path.copy())
                return
            
            neighbors = self.get_neighbors(current)
            for neighbor_info in neighbors:
                neighbor = neighbor_info['to']
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs_paths(neighbor, target, path, visited)
                    path.pop()
                    visited.remove(neighbor)
        
        if self.node_exists(start_node) and self.node_exists(end_node):
            dfs_paths(start_node, end_node, [start_node], {start_node})
        
        return all_paths
    
    def shortest_path(self, start_node: str, end_node: str) -> Dict[str, Any]:
        """
        Find shortest path between two nodes (unweighted or weighted)
        
        Returns:
            Dictionary with 'path' and 'distance'
        """
        if self.weighted:
            return self._dijkstra(start_node, end_node)
        else:
            result = self.bfs(start_node, end_node)
            return {
                "path": result["path"],
                "distance": len(result["path"]) - 1 if result["path"] else float('inf')
            }
    
    def _dijkstra(self, start_node: str, end_node: str) -> Dict[str, Any]:
        """Dijkstra's algorithm for weighted shortest path"""
        import heapq
        
        distances = {node: float('inf') for node in self.get_all_nodes()}
        distances[start_node] = 0
        parent = {start_node: None}
        pq = [(0, start_node)]
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == end_node:
                break
            
            neighbors = self.get_neighbors(current)
            for neighbor_info in neighbors:
                neighbor = neighbor_info['to']
                weight = neighbor_info.get('weight', 1.0)
                distance = current_dist + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    parent[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))
        
        path = self._reconstruct_path(parent, start_node, end_node)
        
        return {
            "path": path,
            "distance": distances[end_node]
        }
    
    # ========================================================================
    # Search and Query Operations
    # ========================================================================
    
    def find_nodes(self, predicate) -> List[str]:
        """
        Find nodes matching a predicate function
        
        Args:
            predicate: Function that takes (node_id, node_data) and returns bool
            
        Returns:
            List of matching node IDs
        """
        matching = []
        
        for node_id in self.get_all_nodes():
            node_data = self.get_node(node_id)
            if predicate(node_id, node_data):
                matching.append(node_id)
        
        return matching
    
    def get_degree(self, node_id: str) -> Dict[str, int]:
        """
        Get degree of a node
        
        Returns:
            Dictionary with 'in_degree', 'out_degree', 'total'
        """
        out_degree = len(self.get_neighbors(node_id))
        
        # Count in-degree
        in_degree = 0
        for node in self.get_all_nodes():
            neighbors = self.get_neighbors(node)
            if any(n['to'] == node_id for n in neighbors):
                in_degree += 1
        
        return {
            "in_degree": in_degree,
            "out_degree": out_degree,
            "total": in_degree + out_degree
        }
    
    # ========================================================================
    # Import/Export Operations
    # ========================================================================
    
    def import_from_json(self, json_str: str) -> bool:
        """
        Import graph from JSON format
        
        JSON format:
        {
            "directed": true,
            "weighted": false,
            "nodes": [
                {"id": "A", "data": {"label": "Node A"}},
                {"id": "B", "data": {"label": "Node B"}}
            ],
            "edges": [
                {"from": "A", "to": "B", "weight": 1.0}
            ]
        }
        """
        try:
            graph_data = json.loads(json_str)
            
            # Clear existing graph
            self.db.clear()
            
            # Set metadata
            self.directed = graph_data.get("directed", True)
            self.weighted = graph_data.get("weighted", False)
            self.db.set("__meta__:directed", str(self.directed))
            self.db.set("__meta__:weighted", str(self.weighted))
            self.db.set("__meta__:node_count", "0")
            self.db.set("__meta__:edge_count", "0")
            
            # Import nodes
            for node in graph_data.get("nodes", []):
                self.add_node(node["id"], node.get("data", {}))
            
            # Import edges
            for edge in graph_data.get("edges", []):
                weight = edge.get("weight", 1.0)
                self.add_edge(edge["from"], edge["to"], weight)
            
            return True
            
        except Exception as e:
            print(f"Error importing JSON: {e}")
            return False
    
    def export_to_json(self, pretty: bool = True) -> str:
        """
        Export graph to JSON format
        
        Args:
            pretty: Pretty print JSON
            
        Returns:
            JSON string representation of the graph
        """
        nodes = []
        for node_id in self.get_all_nodes():
            node_data = self.get_node(node_id)
            nodes.append({
                "id": node_id,
                "data": node_data
            })
        
        edges = []
        for from_node, to_node, weight in self.get_all_edges():
            edge = {"from": from_node, "to": to_node}
            if self.weighted and weight is not None:
                edge["weight"] = weight
            edges.append(edge)
        
        graph_data = {
            "directed": self.directed,
            "weighted": self.weighted,
            "nodes": nodes,
            "edges": edges
        }
        
        if pretty:
            return json.dumps(graph_data, indent=2)
        return json.dumps(graph_data)
    
    def import_from_adjacency_list(self, text: str) -> bool:
        """
        Import graph from adjacency list format
        
        Format:
        A -> B, C
        B -> D
        C -> D, E
        
        For weighted graphs:
        A -> B(1.5), C(2.0)
        """
        try:
            self.db.clear()
            self.db.set("__meta__:directed", str(self.directed))
            self.db.set("__meta__:weighted", str(self.weighted))
            self.db.set("__meta__:node_count", "0")
            self.db.set("__meta__:edge_count", "0")
            
            lines = text.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if '->' in line:
                    parts = line.split('->')
                    from_node = parts[0].strip()
                    
                    # Add source node
                    if not self.node_exists(from_node):
                        self.add_node(from_node)
                    
                    # Parse destinations
                    if len(parts) > 1:
                        destinations = parts[1].split(',')
                        for dest in destinations:
                            dest = dest.strip()
                            
                            # Parse weighted edge: B(1.5)
                            if '(' in dest and ')' in dest:
                                to_node = dest[:dest.index('(')].strip()
                                weight_str = dest[dest.index('(')+1:dest.index(')')].strip()
                                weight = float(weight_str)
                            else:
                                to_node = dest
                                weight = 1.0
                            
                            # Add destination node
                            if not self.node_exists(to_node):
                                self.add_node(to_node)
                            
                            # Add edge
                            self.add_edge(from_node, to_node, weight)
            
            return True
            
        except Exception as e:
            print(f"Error importing adjacency list: {e}")
            return False
    
    def export_to_adjacency_list(self) -> str:
        """
        Export graph to adjacency list format
        
        Returns:
            Adjacency list as string
        """
        lines = []
        
        for node in sorted(self.get_all_nodes()):
            neighbors = self.get_neighbors(node)
            
            if neighbors:
                dest_strs = []
                for neighbor in neighbors:
                    to_node = neighbor['to']
                    if self.weighted and 'weight' in neighbor:
                        dest_strs.append(f"{to_node}({neighbor['weight']})")
                    else:
                        dest_strs.append(to_node)
                
                lines.append(f"{node} -> {', '.join(dest_strs)}")
            else:
                lines.append(f"{node} ->")
        
        return '\n'.join(lines)
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    def get_stats(self) -> Dict[str, Any]:
        """Get graph statistics"""
        return {
            "nodes": int(self.db.get("__meta__:node_count") or "0"),
            "edges": int(self.db.get("__meta__:edge_count") or "0"),
            "directed": self.directed,
            "weighted": self.weighted,
            "db_entries": self.db.count()
        }
    
    def __repr__(self):
        stats = self.get_stats()
        graph_type = "Directed" if self.directed else "Undirected"
        weight_type = "Weighted" if self.weighted else "Unweighted"
        return f"<GraphDB {graph_type}, {weight_type}, {stats['nodes']} nodes, {stats['edges']} edges>"


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    print("Graph Database with Traversal Algorithms")
    print("=" * 60)
    print()
    
    # Create a directed graph
    graph = GraphDB(directed=True, weighted=False)
    
    # Add nodes
    print("Adding nodes...")
    graph.add_node("A", {"label": "Start"})
    graph.add_node("B", {"label": "Middle 1"})
    graph.add_node("C", {"label": "Middle 2"})
    graph.add_node("D", {"label": "Middle 3"})
    graph.add_node("E", {"label": "End"})
    print(f"✓ Added {len(graph.get_all_nodes())} nodes")
    print()
    
    # Add edges
    print("Adding edges...")
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "D")
    graph.add_edge("D", "E")
    graph.add_edge("C", "E")
    print(f"✓ Added edges")
    print()
    
    # Display graph
    print("Graph structure:")
    print(graph.export_to_adjacency_list())
    print()
    
    # BFS traversal
    print("BFS from A to E:")
    bfs_result = graph.bfs("A", "E")
    print(f"  Visited: {bfs_result['visited']}")
    print(f"  Path: {bfs_result['path']}")
    print(f"  Distance: {bfs_result['distances'].get('E', 'N/A')}")
    print()
    
    # DFS traversal
    print("DFS from A to E:")
    dfs_result = graph.dfs("A", "E")
    print(f"  Visited: {dfs_result['visited']}")
    print(f"  Path: {dfs_result['path']}")
    print()
    
    # Find all paths
    print("All paths from A to E:")
    all_paths = graph.find_all_paths("A", "E")
    for i, path in enumerate(all_paths, 1):
        print(f"  Path {i}: {' -> '.join(path)}")
    print()
    
    # Export to JSON
    print("Exporting to JSON...")
    json_export = graph.export_to_json()
    print(json_export)
    print()
    
    # Test weighted graph
    print("\nWeighted Graph Example:")
    print("-" * 60)
    weighted_graph = GraphDB(directed=True, weighted=True)
    
    # Build a weighted graph
    nodes = ["A", "B", "C", "D", "E"]
    for node in nodes:
        weighted_graph.add_node(node)
    
    weighted_graph.add_edge("A", "B", 4.0)
    weighted_graph.add_edge("A", "C", 2.0)
    weighted_graph.add_edge("B", "D", 5.0)
    weighted_graph.add_edge("C", "D", 1.0)
    weighted_graph.add_edge("C", "E", 10.0)
    weighted_graph.add_edge("D", "E", 3.0)
    
    print(weighted_graph.export_to_adjacency_list())
    print()
    
    # Find shortest path
    print("Shortest path from A to E (Dijkstra):")
    shortest = weighted_graph.shortest_path("A", "E")
    print(f"  Path: {' -> '.join(shortest['path'])}")
    print(f"  Total weight: {shortest['distance']}")
    print()
    
    # Graph statistics
    print("Graph Statistics:")
    stats = weighted_graph.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
