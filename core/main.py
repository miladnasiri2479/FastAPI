from fastapi import FastAPI, HTTPException, Path, Body  , Depends , status
from typing import Dict
from sqlalchemy.orm import Session
from schemas import ExpenseSchema
from database import  get_db , Person


app = FastAPI()

expenses: Dict[int , dict] = {}

@app.post("/expenses")
def create_expense(expense: ExpenseSchema, db: Session = Depends(get_db)):
    try:
        new_person = Person(name=expense.name , amount= expense.amount)
        db.add(new_person)
        db.commit()
        db.refresh(new_person) 
        return {
            "status": "success",
            "message": "Object successfully created!",
            "data": {"id": new_person.id, "name": new_person.name}
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An error occurred: {str(e)}")

@app.get("/expenses")
def get_all_expenses(db: Session = Depends(get_db)):
    all_persons= db.query(Person).all()

    return all_persons

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int, db: Session = Depends(get_db)):

    person = db.query(Person).filter(Person.id == expense_id).first()

    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Object not found"
        )

    return person

@app.put("/expenses/{expense_id}")
def update_expense(
    expense: ExpenseSchema, 
    expense_id: int = Path(..., description="شناسه هزینه"), 
    db: Session = Depends(get_db)
):

    db_person=db.query(Person).filter(Person.id == expense_id).first()

    if not db_person:
        raise HTTPException(status_code=404, detail="Object not found, update failed")

    try:

        db_person.name = expense.name
        db_person.amount = expense.amount

        db.commit()
        db.refresh(db_person)

        return {
            "status": "success",
            "message": "Object successfully updated",
            "data": db_person
        }

    except Exception as e:
        db.rollback()
        return {"status": "failed", "message": f"Update failed: {str(e)}"}

@app.delete("/expenses/{expense_id}")
def delete_expense(
                    expense_id: int = Path(..., description="شناسه هزینه"), 
                    db: Session = Depends(get_db)
):
    
    db_person = db.query(Person).filter(Person.id == expense_id).first()

    if not db_person:
        raise HTTPException(status_code=404, detail="Expense not found")

    try:
        db.delete(db_person)
        
        db.commit()

        return {
            "status": "success",
            "message": f"Object with id {expense_id} successfully deleted"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Delete failed: {str(e)}"
        )