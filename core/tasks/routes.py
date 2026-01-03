from fastapi import APIRouter, Path, Depends, HTTPException, Query , Response, Request
from fastapi.responses import JSONResponse
from tasks.schemas import *
from tasks.models import TaskModel
from users.models import UserModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
from auth.jwt_auth import get_authenticated_user , create_access_token , create_refresh_token , verify_token


router = APIRouter(tags=["tasks"])


@router.get("/tasks", response_model=List[TaskResponseSchema])
async def retrieve_tasks_list(
    completed: bool = Query(
        None, description="filter tasks based on being completed or not"
    ),
    limit: int = Query(
        10, gt=0, le=50, description="limiting the number of items to retrieve"
    ),
    offset: int = Query(
        0, ge=0, description="use for paginating based on passed items"
    ),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    query = db.query(TaskModel).filter_by(user_id=user.id)
    if completed is not None:
        query = query.filter_by(is_completed=completed)

    return query.limit(limit).offset(offset).all()



@router.get("/tasks/{task_id}", response_model=TaskResponseSchema)
async def retrieve_task_detail(
    task_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    task_obj = (
        db.query(TaskModel).filter_by(user_id=user.id, id=task_id).first()
    )
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_obj


@router.post("/tasks", response_model=TaskResponseSchema)
async def create_task(
    request: TaskCreateSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    data = request.model_dump()
    data.update({"user_id": user.id})
    task_obj = TaskModel(**data)
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.put("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task(
    request: TaskUpdateSchema,
    task_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    task_obj = (
        db.query(TaskModel).filter_by(user_id=user.id, id=task_id).first()
    )
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields using setattr
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(task_obj, field, value)

    db.commit()  # Commit the changes to the database
    db.refresh(task_obj)  # Refresh the task object to reflect the updated data

    return task_obj  # Return the updated task object


@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(
    task_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    task_obj = (
        db.query(TaskModel).filter_by(user_id=user.id, id=task_id).first()
    )
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_obj)
    db.commit()


@router.post("/login")
async def login(response: Response, login_data: UserLogin, db: Session = Depends(get_db)):
    # ... منطق تایید پسورد کاربر ...
    
    # استفاده از توابعی که قبلا در jwt_auth نوشتی
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    # تنظیم کوکی‌ها طبق خواسته تمرین (HttpOnly و Secure)
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True,   # جلوگیری از حمله XSS
        secure=True,     # ارسال فقط روی HTTPS (در لوکال False بذار)
        samesite="lax"   # جلوگیری از حمله CSRF
    )
    response.set_cookie(
        key="refresh_token", 
        value=refresh_token, 
        httponly=True, 
        secure=True, 
        samesite="lax",
        path="/auth/refresh" # محدود کردن دامنه ارسال ریفرش توکن
    )
    
    return {"message": "ورود موفقیت‌آمیز بود"}
@router.post("/refresh")
async def refresh(request: Request, response: Response):
    # ۱. خواندن ریفرش توکن از کوکی
    rf_token = request.cookies.get("refresh_token")
    if not rf_token:
        raise HTTPException(status_code=401, detail="Refresh token not found")
    
    # ۲. استفاده از تابع verify_token که خودت نوشتی
    # این تابع توکن رو چک میکنه و اگر سالم بود دیتای داخلش رو میده
    token_data = verify_token(rf_token) 
    
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    # ۳. استخراج user_id (چون تو در کدت از user_id استفاده کردی نه sub)
    user_id = token_data.get("user_id")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")
            
    # ۴. تولید اکسس توکن جدید با تابع خودت
    new_access = create_access_token(user_id=user_id)
    
    # ۵. قرار دادن در کوکی
    response.set_cookie(
        key="access_token", 
        value=new_access, 
        httponly=True, 
        secure=False, # در لوکال False
        samesite="lax"
    )
    
    return {"status": "success", "message": "Access token renewed"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "خارج شدید"}