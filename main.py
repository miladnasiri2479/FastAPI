# import FastAPI 
# 
# app = FastAPI()

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Expense Manager API")

# -------------------------
# مدل هزینه
# -------------------------
class Expense(BaseModel):
    description: str
    amount: float


class ExpenseOut(Expense):
    id: int


# -------------------------
# ذخیره‌سازی در حافظه
# -------------------------
expenses: dict[int, ExpenseOut] = {}
current_id = 1


# -------------------------
# ایجاد هزینه جدید (CREATE)
# -------------------------
@app.post("/expenses", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(expense: Expense):
    global current_id

    new_expense = ExpenseOut(
        id=current_id,
        description=expense.description,
        amount=expense.amount
    )

    expenses[current_id] = new_expense
    current_id += 1

    return new_expense


# -------------------------
# دریافت همه هزینه‌ها (READ ALL)
# -------------------------
@app.get("/expenses", response_model=list[ExpenseOut])
def get_all_expenses():
    return list(expenses.values())


# -------------------------
# دریافت یک هزینه با ID (READ ONE)
# -------------------------
@app.get("/expenses/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expenses[expense_id]


# -------------------------
# ویرایش هزینه (UPDATE)
# -------------------------
@app.put("/expenses/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, updated_expense: Expense):
    if expense_id not in expenses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    expense = ExpenseOut(
        id=expense_id,
        description=updated_expense.description,
        amount=updated_expense.amount
    )

    expenses[expense_id] = expense
    return expense


# -------------------------
# حذف هزینه (DELETE)
# -------------------------
@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    del expenses[expense_id]


