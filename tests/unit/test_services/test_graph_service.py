"""
Unit Tests for GraphService

Tests the business logic layer independent of HTTP/Flask.
"""

import pytest
from src.services import (
    GraphService,
    NodeNotFoundError,
    EdgeNotFoundError,
    ValidationError,
    InvalidOperationError,
)


class TestGraphServiceNodeOperations:
    """Test node CRUD operations"""
    
    def test_add_node_success(self):
        """Test successfully adding a node"""
        service = GraphService()
        result = service.add_node("A", {"label": "Node A"})
        
        assert result.node_id == "A"
        assert result.properties["label"] == "Node A"
    
    def test_add_duplicate_node_raises_error(self):
        """Test that adding duplicate node raises error"""
        service = GraphService()
        service.add_node("A")
        
        with pytest.raises(InvalidOperationError, match="already exists"):
            service.add_node("A")
    
    def test_add_node_invalid_id_raises_error(self):
        """Test that invalid node ID raises error"""
        service = GraphService()
        
        with pytest.raises(ValidationError):
            service.add_node("")
        
        with pytest.raises(ValidationError):
            service.add_node("x" * 300)  # Too long
    
    def test_get_node_success(self):
        """Test getting an existing node"""
        service = GraphService()
        service.add_node("A")
        
        result = service.get_node("A")
        assert result.node_id == "A"
    
    def test_get_nonexistent_node_raises_error(self):
        """Test that getting nonexistent node raises error"""
        service = GraphService()
        
        with pytest.raises(NodeNotFoundError, match="not found"):
            service.get_node("Z")
    
    def test_delete_node_success(self):
        """Test deleting a node"""
        service = GraphService()
        service.add_node("A")
        
        result = service.delete_node("A")
        assert result is True
        
        # Verify node is gone
        with pytest.raises(NodeNotFoundError):
            service.get_node("A")
    
    def test_delete_nonexistent_node_raises_error(self):
        """Test that deleting nonexistent node raises error"""
        service = GraphService()
        
        with pytest.raises(NodeNotFoundError):
            service.delete_node("Z")
    
    def test_list_nodes(self):
        """Test listing all nodes"""
        service = GraphService()
        service.add_node("A")
        service.add_node("B")
        service.add_node("C")
        
        nodes = service.list_nodes()
        node_ids = [n.node_id for n in nodes]
        
        assert len(nodes) == 3
        assert set(node_ids) == {"A", "B", "C"}


class TestGraphServiceEdgeOperations:
    """Test edge CRUD operations"""
    
    def test_add_edge_success(self):
        """Test successfully adding an edge"""
        service = GraphService()
        service.add_node("A")
        service.add_node("B")
        
        result = service.add_edge("A", "B", weight=2.5, label="connects")
        
        assert result.from_node == "A"
        assert result.to_node == "B"
        assert result.weight == 2.5
        assert result.label == "connects"
    
    def test_add_edge_nonexistent_node_raises_error(self):
        """Test that adding edge with nonexistent node raises error"""
        service = GraphService()
        service.add_node("A")
        
        with pytest.raises(NodeNotFoundError, match="Target node"):
            service.add_edge("A", "Z")
        
        with pytest.raises(NodeNotFoundError, match="Source node"):
            service.add_edge("Z", "A")
    
    def test_add_edge_invalid_weight_raises_error(self):
        """Test that invalid weight raises error"""
        service = GraphService()
        service.add_node("A")
        service.add_node("B")
        
        with pytest.raises(ValidationError, match="weight must be positive"):
            service.add_edge("A", "B", weight=0)
        
        with pytest.raises(ValidationError):
            service.add_edge("A", "B", weight=-1)
    
    def test_get_edges(self):
        """Test getting all edges"""
        service = GraphService()
        service.add_node("A")
        service.add_node("B")
        service.add_node("C")
        service.add_edge("A", "B")
        service.add_edge("B", "C")
        
        edges = service.get_edges()
        
        assert len(edges) == 2
    
    def test_get_edges_for_node(self):
        """Test getting edges for a specific node"""
        service = GraphService()
        service.add_node("A")
        service.add_node("B")
        service.add_node("C")
        service.add_edge("A", "B")
        service.add_edge("B", "C")
        
        edges = service.get_edges("B")
        
        assert len(edges) == 2  # B->C and A->B


class TestGraphServiceAlgorithms:
    """Test graph algorithms"""
    
    def test_bfs(self):
        """Test breadth-first search"""
        service = GraphService()
        service.add_node("A")
        service.add_node("B")
        service.add_node("C")
        service.add_edge("A", "B")
        service.add_edge("A", "C")
        
        result = service.bfs("A")
        
        assert result.order[0] == "A"
        assert set(result.order) == {"A", "B", "C"}
        assert len(result.visited) == 3
    
    def test_bfs_nonexistent_start_raises_error(self):
        """Test BFS with nonexistent start node"""
        service = GraphService()
        
        with pytest.raises(NodeNotFoundError):
            service.bfs("Z")
    
    def test_dfs(self):
        """Test depth-first search"""
        service = GraphService()
        service.add_node("A")
        service.add_node("B")
        service.add_node("C")
        service.add_edge("A", "B")
        service.add_edge("A", "C")
        
        result = service.dfs("A")
        
        assert result.order[0] == "A"
        assert set(result.order) == {"A", "B", "C"}
    
    def test_shortest_path(self):
        """Test shortest path algorithm"""
        service = GraphService()
        service.add_node("A")
        service.add_node("B")
        service.add_node("C")
        service.add_edge("A", "B", weight=1.0)
        service.add_edge("B", "C", weight=1.0)
        
        result = service.shortest_path("A", "C")
        
        assert result.path == ["A", "B", "C"]
        assert result.cost == 2.0
    
    def test_shortest_path_no_path_raises_error(self):
        """Test shortest path when no path exists"""
        service = GraphService()
        service.add_node("A")
        service.add_node("B")
        # No edge between A and B
        
        with pytest.raises(InvalidOperationError, match="No path exists"):
            service.shortest_path("A", "B")


class TestGraphServiceStatistics:
    """Test graph statistics and queries"""
    
    def test_get_stats(self):
        """Test getting graph statistics"""
        service = GraphService()
        service.add_node("A")
        service.add_node("B")
        service.add_node("C")
        service.add_edge("A", "B")
        service.add_edge("B", "C")
        
        stats = service.get_stats()
        
        assert stats.node_count == 3
        assert stats.edge_count == 2
        assert stats.avg_degree > 0
    
    def test_get_neighbors(self):
        """Test getting node neighbors"""
        service = GraphService()
        service.add_node("A")
        service.add_node("B")
        service.add_node("C")
        service.add_edge("A", "B")
        service.add_edge("A", "C")
        
        neighbors = service.get_neighbors("A")
        
        assert set(neighbors) == {"B", "C"}
    
    def test_search_nodes(self):
        """Test searching for nodes"""
        from src.services.models import SearchCriteria
        
        service = GraphService()
        service.add_node("Alice")
        service.add_node("Bob")
        service.add_node("Charlie")
        
        criteria = SearchCriteria(pattern="li", case_sensitive=False)
        result = service.search_nodes(criteria)
        
        node_ids = [n.node_id for n in result.nodes]
        assert "Alice" in node_ids
        assert "Charlie" in node_ids
        assert "Bob" not in node_ids
    
    def test_clear_graph(self):
        """Test clearing the graph"""
        service = GraphService()
        service.add_node("A")
        service.add_node("B")
        service.add_edge("A", "B")
        
        service.clear()
        
        stats = service.get_stats()
        assert stats.node_count == 0
        assert stats.edge_count == 0


class TestGraphServiceIntegration:
    """Integration tests for service layer"""
    
    def test_complete_workflow(self):
        """Test a complete workflow with multiple operations"""
        service = GraphService()
        
        # Build a graph
        service.add_node("Start")
        service.add_node("Middle")
        service.add_node("End")
        
        service.add_edge("Start", "Middle", weight=1.0)
        service.add_edge("Middle", "End", weight=2.0)
        
        # Query the graph
        stats = service.get_stats()
        assert stats.node_count == 3
        assert stats.edge_count == 2
        
        # Run algorithm
        path = service.shortest_path("Start", "End")
        assert path.path == ["Start", "Middle", "End"]
        
        # Clean up
        service.delete_node("Middle")
        stats = service.get_stats()
        assert stats.node_count == 2
