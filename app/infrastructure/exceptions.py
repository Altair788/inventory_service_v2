"""Custom exceptions for the application."""


class BusinessException(Exception):
    """Base exception for business logic errors."""

    pass


class ItemNotFoundException(BusinessException):
    """Exception raised when an item is not found."""

    pass


class OrderNotFoundException(BusinessException):
    """Exception raised when an order is not found."""

    pass


class ClientNotFoundException(BusinessException):
    """Exception raised when a client is not found."""

    pass


class InsufficientStockException(BusinessException):
    """Exception raised when there is insufficient stock."""

    pass


class CategoryNotFoundException(BusinessException):
    """Exception raised when a category is not found."""

    pass


class DatabaseException(BusinessException):
    """Exception raised for database errors."""

    pass
