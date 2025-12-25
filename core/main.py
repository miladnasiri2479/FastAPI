from fastapi import FastAPI, HTTPException, Path, Body
from typing import Dict
from schemas import ExpenseSchema
app = FastAPI()

expenses: Dict[int , dict] = {}
next_id = 1

@app.post("/expenses")
def create_expense(expense: ExpenseSchema):
    global next_id
    expenses[next_id] = {
        "id" : next_id,
        "description" : expense.name,
        "amount" : expense.amount 
    }
    next_id += 1
    return expenses[next_id - 1]

@app.get("/expenses")
def get_all_expenses():
    return list(expenses.values())

@app.get("/expenses/{expense_id}")
def get_expense (expense_id : int  = Path(..., description="شناسه هزینه")):
    if expense_id not in expenses :
        raise HTTPException(status_code=404, detail="Expense not found")
    return expenses[expense_id]    

@app.put("/expenses/{expense_id}")
def update_expense(
    expense: ExpenseSchema,
    expense_id: int = Path(..., description="شناسه هزینه")
):
    if expense_id not in expenses :
        raise HTTPException(status_code=404, detail="expense not found")
    expenses[expense_id]["description"] = expense.name
    expenses[expense_id]["amount"] = expense.amount
    return expenses[expense_id]

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int = Path(..., description="شناسه هزینه")):
    if expense_id not in expenses:
        raise HTTPException(status_code=404 , detail="expense not found")
    return expenses.pop(expense_id)