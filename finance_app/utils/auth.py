"""
Authentication and authorization utilities
"""
from fastapi import HTTPException, status
from typing import Optional
from models import UserRole


class RoleChecker:
    """Utility class to check user roles and permissions"""
    
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles
    
    def check_permission(self, user_role: str):
        """Check if user has required permission"""
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(self.allowed_roles)}"
            )
        return True


def check_viewer_access(user_role: str):
    """Check if user has viewer access (all roles)"""
    allowed_roles = [UserRole.VIEWER, UserRole.ANALYST, UserRole.ADMIN]
    return user_role in allowed_roles


def check_analyst_access(user_role: str):
    """Check if user has analyst access"""
    allowed_roles = [UserRole.ANALYST, UserRole.ADMIN]
    if user_role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Analyst role required."
        )
    return True


def check_admin_access(user_role: str):
    """Check if user has admin access"""
    if user_role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin role required."
        )
    return True
