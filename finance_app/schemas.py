"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum


class TransactionType(str, Enum):
    """Transaction type enum"""
    INCOME = "income"
    EXPENSE = "expense"


class UserRole(str, Enum):
    """User role enum"""
    VIEWER = "viewer"
    ANALYST = "analyst"
    ADMIN = "admin"


# ============ Transaction Schemas ============

class TransactionCreate(BaseModel):
    """Schema for creating a transaction"""
    amount: float = Field(..., gt=0, description="Transaction amount must be greater than 0")
    type: TransactionType = Field(..., description="Transaction type: income or expense")
    category: str = Field(..., min_length=1, max_length=50, description="Category of transaction")
    date: datetime = Field(..., description="Date of transaction")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes")
    user_id: int = Field(..., gt=0, description="User ID")

    @field_validator('type')
    def validate_type(cls, v):
        if v not in [TransactionType.INCOME, TransactionType.EXPENSE]:
            raise ValueError('Type must be income or expense')
        return v


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction"""
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[TransactionType] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=500)


class TransactionResponse(BaseModel):
    """Schema for transaction response"""
    id: int
    amount: float
    type: str
    category: str
    date: datetime
    notes: Optional[str]
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ User Schemas ============

class UserCreate(BaseModel):
    """Schema for creating a user"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    role: UserRole = Field(default=UserRole.VIEWER)


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    role: Optional[UserRole] = None


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    username: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Analytics Schemas ============

class SummaryResponse(BaseModel):
    """Schema for overall financial summary"""
    total_income: float
    total_expenses: float
    balance: float
    transaction_count: int


class CategoryItem(BaseModel):
    """Schema for category breakdown item"""
    category: str
    income: float
    expenses: float
    balance: float


class CategorySummaryResponse(BaseModel):
    """Schema for category-wise breakdown"""
    summaries: List[CategoryItem]
    total_income: float
    total_expenses: float


class MonthlyItem(BaseModel):
    """Schema for monthly breakdown item"""
    month: str
    income: float
    expenses: float
    balance: float


class MonthlySummaryResponse(BaseModel):
    """Schema for monthly breakdown"""
    summaries: List[MonthlyItem]
    total_income: float
    total_expenses: float


class CategorySummary(BaseModel):
    """Schema for category-wise summary"""
    category: str
    income: float
    expenses: float
    balance: float


class CategorySummaryResponse(BaseModel):
    """Schema for category summary response"""
    summaries: List[CategorySummary]
    total_income: float
    total_expenses: float


class MonthlySummary(BaseModel):
    """Schema for monthly summary"""
    month: str  # Format: YYYY-MM
    income: float
    expenses: float
    balance: float


class MonthlySummaryResponse(BaseModel):
    """Schema for monthly summary response"""
    summaries: List[MonthlySummary]
    total_income: float
    total_expenses: float
