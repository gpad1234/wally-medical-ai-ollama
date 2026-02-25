"""
Data Transfer Objects (DTOs) for Service Layer

These objects are used to pass data between services and API layers.
They provide type safety and clear interfaces.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Any


@dataclass
class NodeResult:
    """Result object for node operations"""
    node_id: str
    properties: Dict[str, Any] = field(default_factory=dict)
    neighbors: Optional[List[str]] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        result = {
            'node_id': self.node_id,
            'properties': self.properties,
        }
        if self.neighbors is not None:
            result['neighbors'] = self.neighbors
        return result


@dataclass
class EdgeResult:
    """Result object for edge operations"""
    from_node: str
    to_node: str
    weight: float = 1.0
    label: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        result = {
            'from': self.from_node,
            'to': self.to_node,
            'weight': self.weight,
        }
        if self.label:
            result['label'] = self.label
        return result


@dataclass
class PathResult:
    """Result object for path operations"""
    path: List[str]
    cost: float
    edges: List[EdgeResult] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'path': self.path,
            'cost': self.cost,
            'edges': [e.to_dict() for e in self.edges],
            'length': len(self.path),
        }


@dataclass
class TraversalResult:
    """Result object for graph traversal operations"""
    order: List[str]
    visited: Set[str] = field(default_factory=set)
    depth: Dict[str, int] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'order': self.order,
            'visited': list(self.visited),
            'depth': self.depth,
            'node_count': len(self.visited),
        }


@dataclass
class GraphStats:
    """Statistics about the graph"""
    node_count: int
    edge_count: int
    avg_degree: float = 0.0
    is_directed: bool = True
    is_weighted: bool = False
    is_connected: Optional[bool] = None
    diameter: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        result = {
            'nodes': self.node_count,
            'edges': self.edge_count,
            'avg_degree': self.avg_degree,
            'directed': self.is_directed,
            'weighted': self.is_weighted,
        }
        if self.is_connected is not None:
            result['connected'] = self.is_connected
        if self.diameter is not None:
            result['diameter'] = self.diameter
        return result


@dataclass
class SearchCriteria:
    """Criteria for searching nodes"""
    pattern: str
    filters: Dict[str, Any] = field(default_factory=dict)
    limit: int = 100
    offset: int = 0
    case_sensitive: bool = False


@dataclass
class SearchResult:
    """Result of a search operation"""
    nodes: List[NodeResult]
    total_count: int
    offset: int
    limit: int
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'nodes': [n.to_dict() for n in self.nodes],
            'total': self.total_count,
            'offset': self.offset,
            'limit': self.limit,
            'returned': len(self.nodes),
        }


@dataclass
class ImportResult:
    """Result of an import operation"""
    nodes_created: int
    edges_created: int
    errors: List[str] = field(default_factory=list)
    success: bool = True
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'nodes_created': self.nodes_created,
            'edges_created': self.edges_created,
            'errors': self.errors,
            'success': self.success,
            'error_count': len(self.errors),
        }
