"""
Service Layer Package

Provides business logic services that sit between API routes and domain models.
Services are framework-agnostic and can be used by Flask, CLI, or other interfaces.
"""

from src.services.graph_service import GraphService
from src.services.base_service import (
    BaseService,
    ServiceError,
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
    ImportResult,
)

__all__ = [
    # Services
    'GraphService',
    'BaseService',
    # Exceptions
    'ServiceError',
    'NodeNotFoundError',
    'EdgeNotFoundError',
    'ValidationError',
    'InvalidOperationError',
    # Models
    'NodeResult',
    'EdgeResult',
    'PathResult',
    'TraversalResult',
    'GraphStats',
    'SearchCriteria',
    'SearchResult',
    'ImportResult',
]
