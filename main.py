from fastapi import FastAPI, HTTPException, Path, Body
from typing import Dict

app = FastAPI()

expenses: Dict[int , dict] = {}
next_id = 1

@app.post("/expenses")
def create_expense(
    description: str = Body(... ,description="توضیح هزینه" ) ,
    amount: float = Body(..., description="مبلغ هزینه")
):
    global next_id
    expenses[next_id] = {
        "id" : next_id,
        "description" : description,
        "amount" : amount 
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
    expense_id: int = Path(..., description="شناسه هزینه"),
    description: str = Body(..., description="توضیح جدید"),
    amount: float = Body(..., description="مبلغ جدید ")
):
    if expense_id not in expenses :
        raise HTTPException(status_code=404, detail="expense not found")
    expenses[expense_id]["description"] = description
    expenses[expense_id]["amount"] = amount
    return expenses[expense_id]

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int = Path(..., description="شناسه هزینه")):
    if expense_id not in expenses:
        raise HTTPException(status_code=404 , detail="expense not found")
    return expenses.pop(expense_id)