"""
Analytics and summary routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import SummaryResponse, CategorySummaryResponse, MonthlySummaryResponse
from utils.auth import check_analyst_access

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=SummaryResponse)
def get_summary(
    user_id: int = Query(..., gt=0, description="User ID"),
    user_role: str = Query(..., description="Current user role"),
    db: Session = Depends(get_db)
):
    """
    Get overall financial summary for a user (Analyst+ only)
    
    Returns:
    - total_income: Sum of all income transactions
    - total_expenses: Sum of all expense transactions
    - balance: total_income - total_expenses
    - transaction_count: Total number of transactions
    """
    check_analyst_access(user_role)
    
    # Verify user exists
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    summary = crud.get_user_summary(db, user_id)
    return summary


@router.get("/category-wise", response_model=CategorySummaryResponse)
def get_category_summary(
    user_id: int = Query(..., gt=0, description="User ID"),
    user_role: str = Query(..., description="Current user role"),
    db: Session = Depends(get_db)
):
    """
    Get category-wise breakdown of transactions (Analyst+ only)
    
    Returns:
    - List of categories with income, expenses, and balance
    - Total income and expenses across all categories
    """
    check_analyst_access(user_role)
    
    # Verify user exists
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    summary = crud.get_category_wise_summary(db, user_id)
    return summary


@router.get("/monthly", response_model=MonthlySummaryResponse)
def get_monthly_summary(
    user_id: int = Query(..., gt=0, description="User ID"),
    user_role: str = Query(..., description="Current user role"),
    db: Session = Depends(get_db)
):
    """
    Get monthly breakdown of transactions (Analyst+ only)
    
    Returns:
    - List of months with income, expenses, and balance
    - Total income and expenses across all months
    """
    check_analyst_access(user_role)
    
    # Verify user exists
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    summary = crud.get_monthly_summary(db, user_id)
    return summary
