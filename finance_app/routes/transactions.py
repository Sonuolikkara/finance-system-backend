"""
Transaction routes for CRUD operations and filtering
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
from database import get_db
import crud
from schemas import TransactionCreate, TransactionUpdate, TransactionResponse
from utils.auth import check_admin_access, check_analyst_access, check_viewer_access

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: TransactionCreate,
    user_role: str = Query(..., description="Current user role"),
    db: Session = Depends(get_db)
):
    """
    Create a new transaction (Admin only)
    """
    check_admin_access(user_role)
    
    # Verify user exists
    user = crud.get_user(db, transaction.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {transaction.user_id} not found"
        )
    
    db_transaction = crud.create_transaction(db, transaction)
    return db_transaction


@router.get("/", response_model=List[TransactionResponse])
def list_transactions(
    user_id: int = Query(..., gt=0, description="User ID"),
    user_role: str = Query(..., description="Current user role"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    List all transactions for a user (All roles can view)
    """
    check_viewer_access(user_role)
    
    # Verify user exists
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    transactions = crud.get_user_transactions(db, user_id, skip=skip, limit=limit)
    return transactions


@router.get("/filter", response_model=List[TransactionResponse])
def filter_transactions(
    user_id: int = Query(..., gt=0, description="User ID"),
    user_role: str = Query(..., description="Current user role"),
    transaction_type: Optional[str] = Query(None, description="income or expense"),
    category: Optional[str] = Query(None, description="Transaction category"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Filter transactions with multiple criteria (Analyst+ only)
    """
    check_analyst_access(user_role)
    
    # Verify user exists
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Validate transaction type if provided
    if transaction_type and transaction_type not in ["income", "expense"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="transaction_type must be 'income' or 'expense'"
        )
    
    transactions = crud.filter_transactions(
        db,
        user_id=user_id,
        transaction_type=transaction_type,
        category=category,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )
    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    user_role: str = Query(..., description="Current user role"),
    db: Session = Depends(get_db)
):
    """
    Get a specific transaction by ID (All roles can view)
    """
    check_viewer_access(user_role)
    
    transaction = crud.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {transaction_id} not found"
        )
    
    return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    user_role: str = Query(..., description="Current user role"),
    db: Session = Depends(get_db)
):
    """
    Update a transaction (Admin only)
    """
    check_admin_access(user_role)
    
    db_transaction = crud.get_transaction(db, transaction_id)
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {transaction_id} not found"
        )
    
    updated_transaction = crud.update_transaction(db, transaction_id, transaction_update)
    return updated_transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    user_role: str = Query(..., description="Current user role"),
    db: Session = Depends(get_db)
):
    """
    Delete a transaction (Admin only)
    """
    check_admin_access(user_role)
    
    success = crud.delete_transaction(db, transaction_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {transaction_id} not found"
        )
    
    return None
