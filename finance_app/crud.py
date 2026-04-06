"""
CRUD operations for database models
"""
from sqlalchemy.orm import Session
from datetime import datetime
from models import User, Transaction, UserRole, TransactionType
from schemas import TransactionCreate, TransactionUpdate, UserCreate, UserUpdate


# ============ User CRUD ============

def create_user(db: Session, user: UserCreate):
    """Create a new user"""
    db_user = User(
        username=user.username,
        email=user.email,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    """Get all users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    """Update user role"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    if user_update.role:
        db_user.role = user_update.role
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """Delete user and associated transactions"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


# ============ Transaction CRUD ============

def create_transaction(db: Session, transaction: TransactionCreate):
    """Create a new transaction"""
    db_transaction = Transaction(
        amount=transaction.amount,
        type=transaction.type,
        category=transaction.category,
        date=transaction.date,
        notes=transaction.notes,
        user_id=transaction.user_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transaction(db: Session, transaction_id: int):
    """Get transaction by ID"""
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()


def get_user_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get all transactions for a user with pagination"""
    return db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).offset(skip).limit(limit).all()


def filter_transactions(
    db: Session,
    user_id: int,
    transaction_type: str = None,
    category: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    skip: int = 0,
    limit: int = 100
):
    """Filter transactions with multiple criteria"""
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    
    if transaction_type:
        query = query.filter(Transaction.type == transaction_type)
    
    if category:
        query = query.filter(Transaction.category.ilike(f"%{category}%"))
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    return query.offset(skip).limit(limit).all()


def update_transaction(db: Session, transaction_id: int, transaction_update: TransactionUpdate):
    """Update a transaction"""
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction:
        return None
    
    update_data = transaction_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transaction, field, value)
    
    db_transaction.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: int):
    """Delete a transaction"""
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction:
        return False
    
    db.delete(db_transaction)
    db.commit()
    return True


# ============ Analytics ============

def get_user_summary(db: Session, user_id: int):
    """Get overall financial summary for a user"""
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    
    total_income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
    total_expenses = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
    balance = total_income - total_expenses
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "transaction_count": len(transactions)
    }


def get_category_wise_summary(db: Session, user_id: int):
    """Get category-wise breakdown of transactions"""
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    
    categories = {}
    for t in transactions:
        if t.category not in categories:
            categories[t.category] = {"income": 0, "expenses": 0}
        
        if t.type == TransactionType.INCOME:
            categories[t.category]["income"] += t.amount
        else:
            categories[t.category]["expenses"] += t.amount
    
    summaries = []
    total_income = 0
    total_expenses = 0
    
    for category, values in categories.items():
        income = values["income"]
        expenses = values["expenses"]
        balance = income - expenses
        
        summaries.append({
            "category": category,
            "income": income,
            "expenses": expenses,
            "balance": balance
        })
        
        total_income += income
        total_expenses += expenses
    
    # Sort by category name
    summaries.sort(key=lambda x: x["category"])
    
    return {
        "summaries": summaries,
        "total_income": total_income,
        "total_expenses": total_expenses
    }


def get_monthly_summary(db: Session, user_id: int):
    """Get monthly breakdown of transactions"""
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    
    months = {}
    for t in transactions:
        month_key = t.date.strftime("%Y-%m")
        
        if month_key not in months:
            months[month_key] = {"income": 0, "expenses": 0}
        
        if t.type == TransactionType.INCOME:
            months[month_key]["income"] += t.amount
        else:
            months[month_key]["expenses"] += t.amount
    
    summaries = []
    total_income = 0
    total_expenses = 0
    
    for month, values in sorted(months.items()):
        income = values["income"]
        expenses = values["expenses"]
        balance = income - expenses
        
        summaries.append({
            "month": month,
            "income": income,
            "expenses": expenses,
            "balance": balance
        })
        
        total_income += income
        total_expenses += expenses
    
    return {
        "summaries": summaries,
        "total_income": total_income,
        "total_expenses": total_expenses
    }
