from fastapi import  APIRouter , Depends , status
from src.tasks import controller
from src.tasks.dtos import TaskCreate , TaskResponse , AllTasksResponse , OneTaskResponse , TaskUpdate
from src.utils.db import get_db
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.utils.helpers import is_authenticated
from typing import List
task_routes = APIRouter(prefix='/tasks')

 
@task_routes.post('/create_task', response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(body: TaskCreate , db: Session = Depends(get_db) , user:UserModel = Depends(is_authenticated)):
    return controller.create_task(body ,db , user)

@task_routes.get('/get_all_tasks', response_model=AllTasksResponse, status_code=status.HTTP_200_OK)
def get_tasks(db: Session = Depends(get_db) , user:UserModel = Depends(is_authenticated)):
    return controller.get_tasks(db ,user)

@task_routes.get('/get_task_by_id/{id}', response_model=OneTaskResponse, status_code=status.HTTP_200_OK)
def get_task_by_id(id: int , db: Session = Depends(get_db) , user:UserModel = Depends(is_authenticated)):
    return controller.get_task_by_id(id , db)

@task_routes.put('/update_task/{id}', response_model=OneTaskResponse, status_code=status.HTTP_200_OK)
def update_task(id:int , body: TaskUpdate , db: Session = Depends(get_db) , user:UserModel = Depends(is_authenticated)):
    return controller.update_task(id , body , db , user)

@task_routes.delete('/delete_task/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id:int , db: Session = Depends(get_db) , user:UserModel = Depends(is_authenticated)):
    return controller.delete_task(id , db , user)



 
    