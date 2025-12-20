from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from database import get_db, User, Task, Category, Tag, hash_password, verify_password
import uvicorn
from jose import JWTError, jwt
import os

app = FastAPI(title="TODO Service")

SECRET_KEY = os.getenv("SECRET_KEY", "test-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Pydantic модели
class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CategoryCreate(BaseModel):
    name: str
    color: Optional[str] = "#808080"

class CategoryResponse(BaseModel):
    id: int
    name: str
    color: str
    user_id: int
    created_at: str
    
    class Config:
        from_attributes = True

class TagCreate(BaseModel):
    name: str
    color: Optional[str] = "#808080"

class TagResponse(BaseModel):
    id: int
    name: str
    color: str
    created_at: str
    
    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    due_date: Optional[str] = None
    priority: Optional[int] = 1

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    due_date: Optional[str] = None
    priority: Optional[int] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: str
    updated_at: str
    due_date: Optional[str]
    priority: int
    user_id: int
    category: Optional[CategoryResponse]
    tags: List[TagResponse]
    
    class Config:
        from_attributes = True

# Вспомогательные функции
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization[7:]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

# Эндпоинты
@app.post("/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    hashed = hash_password(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {
        "id": db_user.id,
        "email": db_user.email,
        "username": db_user.username,
        "created_at": db_user.created_at.isoformat()
    }

@app.post("/auth/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "created_at": current_user.created_at.isoformat()
    }

@app.post("/categories", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_category = Category(
        name=category.name,
        color=category.color,
        user_id=current_user.id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return {
        "id": db_category.id,
        "name": db_category.name,
        "color": db_category.color,
        "user_id": db_category.user_id,
        "created_at": db_category.created_at.isoformat()
    }

@app.get("/categories", response_model=List[CategoryResponse])
def get_user_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    categories = db.query(Category).filter(Category.user_id == current_user.id).all()
    return [
        {
            "id": cat.id,
            "name": cat.name,
            "color": cat.color,
            "user_id": cat.user_id,
            "created_at": cat.created_at.isoformat()
        }
        for cat in categories
    ]

@app.post("/tags", response_model=TagResponse)
def create_tag(
    tag: TagCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag with this name already exists"
        )
    
    db_tag = Tag(name=tag.name, color=tag.color)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    
    return {
        "id": db_tag.id,
        "name": db_tag.name,
        "color": db_tag.color,
        "created_at": db_tag.created_at.isoformat()
    }

@app.get("/tags", response_model=List[TagResponse])
def get_all_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    return [
        {
            "id": tag.id,
            "name": tag.name,
            "color": tag.color,
            "created_at": tag.created_at.isoformat()
        }
        for tag in tags
    ]

# Эндпоинты для задач
@app.post("/tasks", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Проверка категории
    if task.category_id:
        category = db.query(Category).filter(
            Category.id == task.category_id,
            Category.user_id == current_user.id
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
    
    due_date = None
    if task.due_date:
        due_date = datetime.fromisoformat(task.due_date.replace('Z', '+00:00'))
    
    db_task = Task(
        title=task.title,
        description=task.description,
        user_id=current_user.id,
        category_id=task.category_id,
        due_date=due_date,
        priority=task.priority
    )
    
    if task.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(task.tag_ids)).all()
        db_task.tags = tags
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return format_task_response(db_task)

@app.get("/tasks", response_model=List[TaskResponse])
def get_user_tasks(
    completed: Optional[bool] = None,
    category_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    priority: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Task).filter(Task.user_id == current_user.id)
    
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    if category_id is not None:
        query = query.filter(Task.category_id == category_id)
    
    if tag_id is not None:
        query = query.filter(Task.tags.any(Tag.id == tag_id))
    
    if priority is not None:
        query = query.filter(Task.priority == priority)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    return [format_task_response(task) for task in tasks]

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return format_task_response(task)

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == 'tag_ids':
            tags = db.query(Tag).filter(Tag.id.in_(value)).all()
            task.tags = tags
        elif field == 'due_date' and value:
            task.due_date = datetime.fromisoformat(value.replace('Z', '+00:00'))
        elif field == 'category_id' and value:
            category = db.query(Category).filter(
                Category.id == value,
                Category.user_id == current_user.id
            ).first()
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            task.category_id = value
        elif hasattr(task, field):
            setattr(task, field, value)
    
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    
    return format_task_response(task)

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

# Вспомогательная функция для форматирования ответа задачи
def format_task_response(task: Task) -> dict:
    category = None
    if task.category:
        category = {
            "id": task.category.id,
            "name": task.category.name,
            "color": task.category.color,
            "user_id": task.category.user_id,
            "created_at": task.category.created_at.isoformat()
        }
    
    tags = []
    if task.tags:
        for tag in task.tags:
            tags.append({
                "id": tag.id,
                "name": tag.name,
                "color": tag.color,
                "created_at": tag.created_at.isoformat()
            })
    
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "priority": task.priority,
        "user_id": task.user_id,
        "category": category,
        "tags": tags
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)