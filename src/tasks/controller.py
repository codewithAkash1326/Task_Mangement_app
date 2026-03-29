
from sqlalchemy.orm import Session
from src.tasks.dtos import TaskCreate , TaskUpdate
from src.tasks.models import TaskModel 
from src.user.models import UserModel
from fastapi import HTTPException

def create_task(task: TaskCreate , db: Session , user:UserModel):
    data = task.model_dump()
    new_task = TaskModel(title=data.get('title') , description=data.get('description') , is_completed=data.get('is_completed') , user_id =user.id )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task


def get_tasks(db: Session , user:UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id==user.id).all()
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
    

def update_task(id:int , task: TaskUpdate , db: Session , user:UserModel):
    existing_task = db.query(TaskModel).filter(TaskModel.id == id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if existing_task.user_id != user.id:
        raise HTTPException(status_code=401 , detail="You are not allowed to update this task")
    data = task.model_dump(exclude_unset=True)

    for key , value in data.items():
        setattr(existing_task , key , value)
    
    db.commit()
    db.refresh(existing_task)
    
    return {"status": "Task updated successfully",
            "data": existing_task
        }


def delete_task(id:int , db:Session , user:UserModel):
    task = db.query(TaskModel).filter(TaskModel.id == id).first()

    if not task :
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.user_id != user.id:
        raise HTTPException(status_code=401 , detail="You are not allowed to delete this task")
    
    db.delete(task)
    db.commit() 
    return None


 