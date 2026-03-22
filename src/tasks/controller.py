
from sqlalchemy.orm import Session
from src.tasks.dtos import TaskCreate
from src.tasks.models import TaskModel
from fastapi import HTTPException

def create_task(task: TaskCreate , db: Session):
    data = task.model_dump()
    new_task = TaskModel(title=data.get('title') , description=data.get('description') , is_completed=data.get('is_completed'))
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task


def get_tasks(db: Session):
    tasks = db.query(TaskModel).all()
    return {
        "status": "Tasks retrieved successfully",
        "data": tasks
    }

def get_task_by_id(id:int,db:Session):
    task = db.query(TaskModel).filter(TaskModel.id == id).first()
    if task:
        return {"status": "Task retrieved successfully",
                "data": task
            }
    else:
        raise HTTPException(status_code=404, detail="Task not found") 
    

def update_task(id:int , task: TaskCreate , db: Session):
    existing_task = db.query(TaskModel).filter(TaskModel.id == id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    data = task.model_dump()

    for key , value in data.items():
        setattr(existing_task , key , value)
    
    db.commit()
    db.refresh(existing_task)
    
    return {"status": "Task updated successfully",
            "data": existing_task
        }


def delete_task(id:int , db:Session):
    task = db.query(TaskModel).filter(TaskModel.id == id).first()

    if not task :
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit() 
    return None


def mark_task_as_completed(id:int , db:Session):
    task = db.query(TaskModel).filter(TaskModel.id == id).first()

    if not task :
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.is_completed = True
    db.commit()
    db.refresh(task)

    return {"status": "Task marked as completed successfully",
            "data": task
        }