"""
Graph Service

Business logic for graph database operations.
Provides a clean interface between API routes and GraphDB.
"""

from typing import List, Optional, Dict, Any
from graph_db import GraphDB
from src.services.base_service import (
    BaseService,
    NodeNotFoundError,
    EdgeNotFoundError,
    ValidationError,
    InvalidOperationError,
)
from src.services.models import (
    NodeResult,
    EdgeResult,
    PathResult,
    TraversalResult,
    GraphStats,
    SearchCriteria,
    SearchResult,
)


class GraphService(BaseService):
    """
    Service for graph database operations
    
    Handles:
    - Node and edge CRUD operations
    - Graph algorithms (BFS, DFS, shortest path)
    - Graph queries and statistics
    - Data validation
    """
    
    def __init__(self, graph_db: Optional[GraphDB] = None):
        """
        Initialize graph service
        
        Args:
            graph_db: Optional existing GraphDB instance. Creates new one if not provided.
        """
        super().__init__()
        self.graph = graph_db or GraphDB()
        self._log_debug("GraphService initialized")
    
    # ========================================================================
    # NODE OPERATIONS
    # ========================================================================
    
    def add_node(self, node_id: str, properties: Optional[Dict[str, Any]] = None) -> NodeResult:
        """
        Add a node to the graph
        
        Args:
            node_id: Unique identifier for the node
            properties: Optional node properties/metadata
            
        Returns:
            NodeResult with node information
            
        Raises:
            ValidationError: If node_id is invalid
            InvalidOperationError: If node already exists
        """
        self._validate_node_id(node_id)
        self._log_operation("add_node", node_id=node_id)
        
        if self.graph.node_exists(node_id):
            raise InvalidOperationError(f"Node '{node_id}' already exists")
        
        # Add node to graph
        self.graph.add_node(node_id)
        
        # Store properties if provided
        if properties:
            # In future: store properties in separate system
            pass
        
        return NodeResult(node_id=node_id, properties=properties or {})
    
    def get_node(self, node_id: str) -> NodeResult:
        """
        Get a node by ID
        
        Args:
            node_id: Node identifier
            
        Returns:
            NodeResult with node information
            
        Raises:
            NodeNotFoundError: If node doesn't exist
        """
        self._validate_node_id(node_id)
        
        if not self.graph.node_exists(node_id):
            raise NodeNotFoundError(f"Node '{node_id}' not found")
        
        # Get neighbors
        neighbors = self.graph.get_neighbors(node_id)
        
        return NodeResult(
            node_id=node_id,
            properties={},
            neighbors=neighbors
        )
    
    def delete_node(self, node_id: str) -> bool:
        """
        Delete a node from the graph
        
        Args:
            node_id: Node identifier
            
        Returns:
            True if deleted successfully
            
        Raises:
            NodeNotFoundError: If node doesn't exist
        """
        self._validate_node_id(node_id)
        self._log_operation("delete_node", node_id=node_id)
        
        if not self.graph.node_exists(node_id):
            raise NodeNotFoundError(f"Node '{node_id}' not found")
        
        # Delete the node
        self.graph.delete_node(node_id)
        return True
    
    def list_nodes(self) -> List[NodeResult]:
        """
        Get all nodes in the graph
        
        Returns:
            List of NodeResult objects
        """
        nodes = self.graph.get_all_nodes()
        return [NodeResult(node_id=node_id, properties={}) for node_id in nodes]
    
    # ========================================================================
    # EDGE OPERATIONS
    # ========================================================================
    
    def add_edge(
        self,
        from_node: str,
        to_node: str,
        weight: float = 1.0,
        label: Optional[str] = None
    ) -> EdgeResult:
        """
        Add an edge between two nodes
        
        Args:
            from_node: Source node ID
            to_node: Target node ID
            weight: Edge weight (default 1.0)
            label: Optional edge label
            
        Returns:
            EdgeResult with edge information
            
        Raises:
            NodeNotFoundError: If either node doesn't exist
            ValidationError: If weight is invalid
        """
        self._validate_node_id(from_node)
        self._validate_node_id(to_node)
        
        if weight <= 0:
            raise ValidationError("Edge weight must be positive")
        
        self._log_operation("add_edge", from_node=from_node, to_node=to_node, weight=weight)
        
        # Verify nodes exist
        if not self.graph.node_exists(from_node):
            raise NodeNotFoundError(f"Source node '{from_node}' not found")
        if not self.graph.node_exists(to_node):
            raise NodeNotFoundError(f"Target node '{to_node}' not found")
        
        # Add edge
        self.graph.add_edge(from_node, to_node, weight)
        
        # Note: GraphDB doesn't support edge labels yet - stored in result only
        
        return EdgeResult(
            from_node=from_node,
            to_node=to_node,
            weight=weight,
            label=label
        )
    
    def get_edges(self, node_id: Optional[str] = None) -> List[EdgeResult]:
        """
        Get edges in the graph
        
        Args:
            node_id: Optional node ID to get edges for. If None, returns all edges.
            
        Returns:
            List of EdgeResult objects
        """
        if node_id:
            self._validate_node_id(node_id)
            if not self.graph.node_exists(node_id):
                raise NodeNotFoundError(f"Node '{node_id}' not found")
        
        # Get all edges
        edges = self.graph.get_all_edges()
        
        results = []
        for edge in edges:
            # Filter by node if specified
            if node_id and edge[0] != node_id and edge[1] != node_id:
                continue
            
            results.append(EdgeResult(
                from_node=edge[0],
                to_node=edge[1],
                weight=edge[2],
                label=None
            ))
        
        return results
    
    def delete_edge(self, from_node: str, to_node: str) -> bool:
        """
        Delete an edge from the graph
        
        Args:
            from_node: Source node ID
            to_node: Target node ID
            
        Returns:
            True if deleted successfully
            
        Raises:
            EdgeNotFoundError: If edge doesn't exist
        """
        self._validate_node_id(from_node)
        self._validate_node_id(to_node)
        self._log_operation("delete_edge", from_node=from_node, to_node=to_node)
        
        if not self.graph.edge_exists(from_node, to_node):
            raise EdgeNotFoundError(f"Edge from '{from_node}' to '{to_node}' not found")
        
        self.graph.delete_edge(from_node, to_node)
        return True
    
    # ========================================================================
    # GRAPH ALGORITHMS
    # ========================================================================
    
    def bfs(self, start: str) -> TraversalResult:
        """
        Perform breadth-first search traversal
        
        Args:
            start: Starting node ID
            
        Returns:
            TraversalResult with traversal order and depths
            
        Raises:
            NodeNotFoundError: If start node doesn't exist
        """
        self._validate_node_id(start)
        
        if not self.graph.node_exists(start):
            raise NodeNotFoundError(f"Start node '{start}' not found")
        
        self._log_operation("bfs", start=start)
        
        # Perform BFS
        result = self.graph.bfs(start)
        order = result.get('visited', [])
        depths = result.get('distances', {})
        
        return TraversalResult(
            order=order,
            visited=set(order),
            depth=depths
        )
    
    def dfs(self, start: str) -> TraversalResult:
        """
        Perform depth-first search traversal
        
        Args:
            start: Starting node ID
            
        Returns:
            TraversalResult with traversal order
            
        Raises:
            NodeNotFoundError: If start node doesn't exist
        """
        self._validate_node_id(start)
        
        if not self.graph.node_exists(start):
            raise NodeNotFoundError(f"Start node '{start}' not found")
        
        self._log_operation("dfs", start=start)
        
        # Perform DFS
        result = self.graph.dfs(start)
        order = result.get('visited', [])
        
        return TraversalResult(
            order=order,
            visited=set(order),
            depth={}
        )
    
    def shortest_path(self, start: str, end: str) -> PathResult:
        """
        Find shortest path between two nodes (Dijkstra's algorithm)
        
        Args:
            start: Starting node ID
            end: Target node ID
            
        Returns:
            PathResult with path and cost
            
        Raises:
            NodeNotFoundError: If either node doesn't exist
            InvalidOperationError: If no path exists
        """
        self._validate_node_id(start)
        self._validate_node_id(end)
        
        if not self.graph.node_exists(start):
            raise NodeNotFoundError(f"Start node '{start}' not found")
        if not self.graph.node_exists(end):
            raise NodeNotFoundError(f"End node '{end}' not found")
        
        self._log_operation("shortest_path", start=start, end=end)
        
        # Find shortest path using Dijkstra's algorithm
        result_dict = self.graph._dijkstra(start, end)
        path = result_dict.get("path", [])
        cost = result_dict.get("distance", 0)
        
        if not path:
            raise InvalidOperationError(f"No path exists from '{start}' to '{end}'")
        
        # Build edge list with actual weights
        edges = []
        for i in range(len(path) - 1):
            # Look up actual edge weight
            neighbors = self.graph.get_neighbors(path[i])
            weight = 1.0
            for neighbor_info in neighbors:
                if neighbor_info['to'] == path[i + 1]:
                    weight = neighbor_info.get('weight', 1.0)
                    break
            
            edges.append(EdgeResult(
                from_node=path[i],
                to_node=path[i + 1],
                weight=weight
            ))
        
        return PathResult(path=path, cost=cost, edges=edges)
    
    def all_paths(self, start: str, end: str, max_paths: int = 10) -> List[PathResult]:
        """
        Find all paths between two nodes
        
        Args:
            start: Starting node ID
            end: Target node ID
            max_paths: Maximum number of paths to return
            
        Returns:
            List of PathResult objects
            
        Raises:
            NodeNotFoundError: If either node doesn't exist
        """
        self._validate_node_id(start)
        self._validate_node_id(end)
        
        if not self.graph.node_exists(start):
            raise NodeNotFoundError(f"Start node '{start}' not found")
        if not self.graph.node_exists(end):
            raise NodeNotFoundError(f"End node '{end}' not found")
        
        self._log_operation("all_paths", start=start, end=end)
        
        # Find all paths
        paths = self.graph.all_paths(start, end)[:max_paths]
        
        results = []
        for path in paths:
            # Calculate cost (sum of edge weights)
            cost = len(path) - 1  # Simplified
            results.append(PathResult(path=path, cost=cost, edges=[]))
        
        return results
    
    # ========================================================================
    # QUERIES & STATISTICS
    # ========================================================================
    
    def get_stats(self) -> GraphStats:
        """
        Get graph statistics
        
        Returns:
            GraphStats object with graph metrics
        """
        nodes = self.graph.get_all_nodes()
        edges = self.graph.get_all_edges()
        
        node_count = len(nodes)
        edge_count = len(edges)
        
        # Calculate average degree
        if node_count > 0:
            total_degree = sum(len(self.graph.get_neighbors(n)) for n in nodes)
            avg_degree = total_degree / node_count
        else:
            avg_degree = 0.0
        
        return GraphStats(
            node_count=node_count,
            edge_count=edge_count,
            avg_degree=avg_degree,
            is_directed=self.graph.directed,
            is_weighted=self.graph.weighted
        )
    
    def get_neighbors(self, node_id: str) -> List[str]:
        """
        Get neighbors of a node
        
        Args:
            node_id: Node identifier
            
        Returns:
            List of neighbor node IDs
            
        Raises:
            NodeNotFoundError: If node doesn't exist
        """
        self._validate_node_id(node_id)
        
        if not self.graph.node_exists(node_id):
            raise NodeNotFoundError(f"Node '{node_id}' not found")
        
        # Get neighbors and extract just the node IDs
        neighbors_data = self.graph.get_neighbors(node_id)
        return [neighbor['to'] for neighbor in neighbors_data]
    
    def search_nodes(self, criteria: SearchCriteria) -> SearchResult:
        """
        Search for nodes matching criteria
        
        Args:
            criteria: Search criteria
            
        Returns:
            SearchResult with matching nodes
        """
        self._log_operation("search_nodes", pattern=criteria.pattern)
        
        all_nodes = self.graph.get_all_nodes()
        pattern = criteria.pattern.lower() if not criteria.case_sensitive else criteria.pattern
        
        # Filter nodes
        matching = []
        for node_id in all_nodes:
            node_id_cmp = node_id.lower() if not criteria.case_sensitive else node_id
            if pattern in node_id_cmp:
                matching.append(node_id)
        
        total = len(matching)
        
        # Apply pagination
        start = criteria.offset
        end = start + criteria.limit
        paginated = matching[start:end]
        
        # Convert to NodeResult
        nodes = [NodeResult(node_id=nid, properties={}) for nid in paginated]
        
        return SearchResult(
            nodes=nodes,
            total_count=total,
            offset=criteria.offset,
            limit=criteria.limit
        )
    
    def clear(self) -> None:
        """Clear all nodes and edges from the graph"""
        self._log_operation("clear")
        # GraphDB doesn't have clear(), so we need to delete all nodes
        nodes = self.graph.get_all_nodes()
        for node_id in nodes:
            self.graph.delete_node(node_id)
