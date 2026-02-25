"""
Base Service Class

Provides common functionality for all service classes.
"""

import logging
from typing import Any, Dict


class ServiceError(Exception):
    """Base exception for service layer errors"""
    pass


class NodeNotFoundError(ServiceError):
    """Raised when a node doesn't exist"""
    pass


class EdgeNotFoundError(ServiceError):
    """Raised when an edge doesn't exist"""
    pass


class ValidationError(ServiceError):
    """Raised when validation fails"""
    pass


class InvalidOperationError(ServiceError):
    """Raised when an operation is not allowed"""
    pass


class BaseService:
    """
    Base class for all services
    
    Provides:
    - Logging
    - Common error handling
    - Operation tracking
    """
    
    def __init__(self):
        """Initialize base service"""
        self._logger = logging.getLogger(self.__class__.__name__)
        self._operation_count = 0
    
    def _log_operation(self, operation: str, **kwargs: Any) -> None:
        """
        Log a service operation
        
        Args:
            operation: Name of the operation
            **kwargs: Additional context to log
        """
        self._operation_count += 1
        self._logger.info(f"Operation #{self._operation_count}: {operation}", extra=kwargs)
    
    def _log_debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message"""
        self._logger.debug(message, extra=kwargs)
    
    def _log_warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message"""
        self._logger.warning(message, extra=kwargs)
    
    def _log_error(self, message: str, **kwargs: Any) -> None:
        """Log error message"""
        self._logger.error(message, extra=kwargs)
    
    def _handle_error(self, error: Exception, context: str) -> None:
        """
        Centralized error handling
        
        Args:
            error: The exception that occurred
            context: Description of what was being done
            
        Raises:
            ServiceError: Wraps the original error
        """
        self._log_error(f"Error in {context}: {str(error)}", error_type=type(error).__name__)
        raise ServiceError(f"{context} failed: {str(error)}") from error
    
    def _validate_required(self, data: Dict[str, Any], required_fields: list) -> None:
        """
        Validate required fields are present
        
        Args:
            data: Dictionary to validate
            required_fields: List of required field names
            
        Raises:
            ValidationError: If any required field is missing
        """
        missing = [field for field in required_fields if field not in data]
        if missing:
            raise ValidationError(f"Missing required fields: {', '.join(missing)}")
    
    def _validate_node_id(self, node_id: str) -> None:
        """
        Validate node ID format
        
        Args:
            node_id: Node identifier to validate
            
        Raises:
            ValidationError: If node_id is invalid
        """
        if not node_id or not isinstance(node_id, str):
            raise ValidationError("Node ID must be a non-empty string")
        
        if len(node_id) > 256:
            raise ValidationError("Node ID too long (max 256 characters)")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get service statistics
        
        Returns:
            Dictionary with service stats
        """
        return {
            'service_name': self.__class__.__name__,
            'operations_processed': self._operation_count,
        }
