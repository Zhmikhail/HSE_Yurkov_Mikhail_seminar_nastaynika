from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Table, Enum, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
import bcrypt

os.makedirs('/app/data', exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:////app/data/todo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Ассоциативная таблица для тегов и задач
task_tags = Table('task_tags', Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

# Типы связей между задачами
class TaskRelationType(Enum):
    PARENT = "parent"          # родительская задача
    CHILD = "child"            # дочерняя задача
    BLOCKS = "blocks"          # блокирует
    BLOCKED_BY = "blocked_by"  # блокируется
    RELATED = "related"        # связанная
    DUPLICATE = "duplicate"    # дубликат

# Модель пользователя
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Связи
    tasks = relationship("Task", back_populates="owner")
    categories = relationship("Category", back_populates="owner")

# Модель категории
class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    color = Column(String, default="#808080")  # цвет для UI
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    owner = relationship("User", back_populates="categories")
    tasks = relationship("Task", back_populates="category")

# Модель тега
class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    color = Column(String, default="#808080")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    tasks = relationship("Task", secondary=task_tags, back_populates="tags")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    priority = Column(Integer, default=1)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    
    # Связи
    owner = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")
    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")
    
    # Связи с другими задачами
    related_tasks = relationship(
        "TaskRelation",
        foreign_keys="TaskRelation.task_from_id",
        backref="task_from_ref"
    )
    related_by_tasks = relationship(
        "TaskRelation", 
        foreign_keys="TaskRelation.task_to_id",
        backref="task_to_ref"
    )

# Модель связи между задачами
class TaskRelation(Base):
    __tablename__ = "task_relations"
    
    id = Column(Integer, primary_key=True, index=True)
    task_from_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    task_to_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    relation_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    task_from = relationship("Task", foreign_keys=[task_from_id], viewonly=True)
    task_to = relationship("Task", foreign_keys=[task_to_id], viewonly=True)

Base.metadata.create_all(bind=engine)

# Функции для работы с паролями
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()