"""
Graph Pagination Service - Proof of Concept

Demonstrates paginated graph access and fish-eye viewport loading.
This is a lightweight implementation that works with existing graph_db.py
"""

from typing import Dict, List, Set, Any, Optional
from collections import deque


class GraphPaginationService:
    """
    Service for efficient paginated access to graph data
    
    Features:
    - Paginated node retrieval (skip/limit)
    - Viewport-based loading (fish-eye center + radius)
    - Neighbor expansion for progressive disclosure
    - Type-based filtering
    """
    
    def __init__(self, graph_db):
        """
        Initialize with existing graph database
        
        Args:
            graph_db: GraphDB instance
        """
        self.graph = graph_db
        self._build_indexes()
    
    def _build_indexes(self):
        """Build lookup indexes for fast access"""
        self.node_index = {}  # id -> node data
        self.type_index = {}  # type -> [node_ids]
        self.edge_index = {}  # node_id -> [(target_id, edge_data)]
        
        # Build node indexes
        # get_all_nodes() returns list of node IDs, not node objects
        all_node_ids = self.graph.get_all_nodes()
        for node_id in all_node_ids:
            node = self.graph.get_node(node_id)
            if node:
                self.node_index[node_id] = node
                
                # Index by type
                node_type = node.get('data', {}).get('node_type', 'unknown')
                if node_type not in self.type_index:
                    self.type_index[node_type] = []
                self.type_index[node_type].append(node_id)
        
        # Build edge index
        # Note: graph_db doesn't have get_all_edges, so we'll use adjacency
        for node_id in self.node_index:
            self.edge_index[node_id] = []
            neighbors = self.graph.get_neighbors(node_id)
            for neighbor_dict in neighbors:
                # get_neighbors returns list of dicts with 'to' key
                target_id = neighbor_dict.get('to') if isinstance(neighbor_dict, dict) else neighbor_dict
                if target_id:
                    self.edge_index[node_id].append({
                        'target': target_id,
                        'type': 'connected'
                    })
    
    def get_page(
        self,
        skip: int = 0,
        limit: int = 50,
        node_type: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get paginated nodes
        
        Args:
            skip: Number of nodes to skip
            limit: Maximum nodes to return
            node_type: Filter by node type (e.g., 'owl:Class')
            search_query: Search in labels/IDs
        
        Returns:
            {
                'nodes': [...],
                'edges': [...],
                'total': int,
                'skip': int,
                'limit': int,
                'has_more': bool
            }
        """
        # Get filtered node IDs
        if node_type:
            node_ids = self.type_index.get(node_type, [])
        else:
            node_ids = list(self.node_index.keys())
        
        # Apply search filter
        if search_query:
            query_lower = search_query.lower()
            node_ids = [
                nid for nid in node_ids
                if query_lower in nid.lower() or
                   query_lower in self.node_index[nid].get('data', {}).get('label', '').lower()
            ]
        
        # Sort for consistency
        node_ids.sort()
        
        # Calculate pagination
        total = len(node_ids)
        page_ids = node_ids[skip:skip + limit]
        
        # Get nodes and their edges
        nodes = [self._format_node(nid) for nid in page_ids]
        edges = self._get_edges_for_nodes(page_ids)
        
        return {
            'nodes': nodes,
            'edges': edges,
            'total': total,
            'skip': skip,
            'limit': limit,
            'has_more': skip + limit < total,
            'page': skip // limit + 1,
            'total_pages': (total + limit - 1) // limit
        }
    
    def get_viewport(
        self,
        center_id: str,
        radius: int = 2,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Get nodes within radius hops of center node (fish-eye view)
        
        This implements the "focus + context" pattern:
        - Center node is at focus (radius 0)
        - Neighbors at increasing distances provide context
        - Limit prevents loading too many nodes
        
        Args:
            center_id: ID of center/focus node
            radius: Number of hops to traverse
            limit: Maximum total nodes to return
        
        Returns:
            {
                'center': str,
                'radius': int,
                'nodes': [...],
                'edges': [...],
                'levels': {0: [...], 1: [...], ...}  # Nodes by distance
            }
        """
        if not self.graph.node_exists(center_id):
            return {
                'error': f'Node {center_id} not found',
                'nodes': [],
                'edges': []
            }
        
        # BFS to find nodes within radius
        visited = {center_id}
        levels = {0: [center_id]}  # Distance -> [node_ids]
        current_level = [center_id]
        
        for distance in range(1, radius + 1):
            next_level = []
            
            for node_id in current_level:
                # Get neighbors (bidirectional - follow edges in both directions)
                # Forward edges: node_id -> target
                forward_neighbors = [
                    edge['target'] 
                    for edge in self.edge_index.get(node_id, [])
                ]
                
                # Backward edges: source -> node_id (node_id is target)
                backward_neighbors = [
                    source_id
                    for source_id, edges in self.edge_index.items()
                    for edge in edges
                    if edge['target'] == node_id
                ]
                
                # Combine both directions
                neighbors = forward_neighbors + backward_neighbors
                
                for neighbor_id in neighbors:
                    if neighbor_id not in visited:
                        visited.add(neighbor_id)
                        next_level.append(neighbor_id)
                
                # Check limit
                if len(visited) >= limit:
                    break
            
            levels[distance] = next_level
            current_level = next_level
            
            if len(visited) >= limit:
                break
        
        # Collect all node IDs up to limit
        all_node_ids = []
        for distance in sorted(levels.keys()):
            all_node_ids.extend(levels[distance])
            if len(all_node_ids) >= limit:
                break
        
        all_node_ids = all_node_ids[:limit]
        
        # Get nodes and edges
        nodes = [self._format_node(nid) for nid in all_node_ids]
        edges = self._get_edges_for_nodes(all_node_ids)
        
        # Add distance metadata to nodes
        for node in nodes:
            node_id = node['id']
            for distance, node_list in levels.items():
                if node_id in node_list:
                    node['distance_from_center'] = distance
                    break
        
        return {
            'center': center_id,
            'radius': radius,
            'nodes': nodes,
            'edges': edges,
            'levels': {d: len(nodes) for d, nodes in levels.items()},
            'total_nodes': len(nodes)
        }
    
    def get_neighbors(
        self,
        node_id: str,
        depth: int = 1
    ) -> Dict[str, Any]:
        """
        Get immediate neighbors of a node
        
        Used for progressive expansion when user clicks a node
        
        Args:
            node_id: ID of node to get neighbors for
            depth: How many hops (usually 1)
        
        Returns:
            {
                'node_id': str,
                'neighbors': [...],
                'edges': [...]
            }
        """
        if not self.graph.node_exists(node_id):
            return {
                'error': f'Node {node_id} not found',
                'neighbors': []
            }
        
        # Get direct neighbors (depth=1)
        neighbor_ids = [
            edge['target']
            for edge in self.edge_index.get(node_id, [])
        ]
        
        neighbors = [self._format_node(nid) for nid in neighbor_ids]
        edges = self._get_edges_for_nodes([node_id] + neighbor_ids)
        
        return {
            'node_id': node_id,
            'neighbors': neighbors,
            'edges': edges,
            'count': len(neighbors)
        }
    
    def search(
        self,
        query: str,
        skip: int = 0,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search for nodes matching query
        
        Args:
            query: Search string (matches ID and label)
            skip: Pagination skip
            limit: Max results
        
        Returns:
            Paginated search results
        """
        return self.get_page(
            skip=skip,
            limit=limit,
            search_query=query
        )
    
    def _format_node(self, node_id: str) -> Dict[str, Any]:
        """Format node for API response"""
        node = self.node_index.get(node_id, {})
        return {
            'id': node_id,
            'label': node.get('data', {}).get('label', node_id),
            'type': node.get('data', {}).get('node_type', 'unknown'),
            'data': node.get('data', {}),
            'metadata': {
                'neighbor_count': len(self.edge_index.get(node_id, []))
            }
        }
    
    def _get_edges_for_nodes(self, node_ids: List[str]) -> List[Dict[str, Any]]:
        """Get edges between nodes in the list (bidirectional)"""
        node_set = set(node_ids)
        edges = []
        seen_edges = set()  # Track (source, target) pairs to avoid duplicates
        
        for source_id in node_ids:
            for edge in self.edge_index.get(source_id, []):
                target_id = edge['target']
                # Only include edges where both nodes are in our set
                if target_id in node_set:
                    edge_key = (source_id, target_id)
                    if edge_key not in seen_edges:
                        seen_edges.add(edge_key)
                        edges.append({
                            'source': source_id,
                            'target': target_id,
                            'type': edge.get('type', 'connected')
                        })
        
        return edges
    
    def get_stats(self) -> Dict[str, Any]:
        """Get graph statistics"""
        return {
            'total_nodes': len(self.node_index),
            'total_edges': sum(len(edges) for edges in self.edge_index.values()),
            'node_types': {
                node_type: len(nodes)
                for node_type, nodes in self.type_index.items()
            }
        }


# Example usage
if __name__ == '__main__':
    # Mock graph_db for testing
    class MockGraphDB:
        def __init__(self):
            self.nodes = {
                'owl:Thing': {'id': 'owl:Thing', 'data': {'label': 'Thing', 'node_type': 'owl:Class'}},
                'demo:Person': {'id': 'demo:Person', 'data': {'label': 'Person', 'node_type': 'owl:Class'}},
                'demo:Student': {'id': 'demo:Student', 'data': {'label': 'Student', 'node_type': 'owl:Class'}},
                'demo:Professor': {'id': 'demo:Professor', 'data': {'label': 'Professor', 'node_type': 'owl:Class'}},
            }
            self.edges = {
                'demo:Person': ['demo:Student', 'demo:Professor'],
                'owl:Thing': ['demo:Person']
            }
        
        def get_all_nodes(self):
            return list(self.nodes.values())
        
        def node_exists(self, node_id):
            return node_id in self.nodes
        
        def get_neighbors(self, node_id):
            return self.edges.get(node_id, [])
    
    # Test pagination service
    graph = MockGraphDB()
    service = GraphPaginationService(graph)
    
    print("=== Graph Stats ===")
    print(service.get_stats())
    
    print("\n=== Page 1 (limit=2) ===")
    page1 = service.get_page(skip=0, limit=2)
    print(f"Nodes: {[n['id'] for n in page1['nodes']]}")
    print(f"Total: {page1['total']}, Has More: {page1['has_more']}")
    
    print("\n=== Viewport around demo:Person (radius=2) ===")
    viewport = service.get_viewport('demo:Person', radius=2, limit=10)
    print(f"Center: {viewport['center']}")
    print(f"Nodes: {[n['id'] for n in viewport['nodes']]}")
    print(f"Levels: {viewport['levels']}")
    
    print("\n=== Neighbors of demo:Person ===")
    neighbors = service.get_neighbors('demo:Person')
    print(f"Neighbors: {[n['id'] for n in neighbors['neighbors']]}")
