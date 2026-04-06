"""
User management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import crud
from schemas import UserCreate, UserUpdate, UserResponse
from utils.auth import check_admin_access

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    user_role: str = Query(..., description="Current user role"),
    db: Session = Depends(get_db)
):
    """
    Create a new user (Admin only)
    """
    check_admin_access(user_role)
    
    # Check if username already exists
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{user.username}' already exists"
        )
    
    db_user = crud.create_user(db, user)
    return db_user


@router.get("/", response_model=List[UserResponse])
def list_users(
    user_role: str = Query(..., description="Current user role"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    List all users (Admin only)
    """
    check_admin_access(user_role)
    
    users = crud.get_all_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    user_role: str = Query(..., description="Current user role"),
    db: Session = Depends(get_db)
):
    """
    Get a specific user by ID (Admin only)
    """
    check_admin_access(user_role)
    
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_role: str = Query(..., description="Current user role"),
    db: Session = Depends(get_db)
):
    """
    Update user role (Admin only)
    """
    check_admin_access(user_role)
    
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    updated_user = crud.update_user(db, user_id, user_update)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    user_role: str = Query(..., description="Current user role"),
    db: Session = Depends(get_db)
):
    """
    Delete a user and all associated transactions (Admin only)
    """
    check_admin_access(user_role)
    
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    return None
