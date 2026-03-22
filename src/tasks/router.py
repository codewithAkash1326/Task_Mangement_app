from fastapi import  APIRouter , Depends , status
from src.tasks import controller
from src.tasks.dtos import TaskCreate , TaskResponse , AllTasksResponse , OneTaskResponse
from src.utils.db import get_db
from sqlalchemy.orm import Session
from typing import List
task_routes = APIRouter(prefix='/tasks')

 
@task_routes.post('/create_task', response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(body: TaskCreate , db: Session = Depends(get_db)):
    return controller.create_task(body ,db)

@task_routes.get('/get_all_tasks', response_model=AllTasksResponse, status_code=status.HTTP_200_OK)
def get_tasks(db: Session = Depends(get_db)):
    return controller.get_tasks(db)

@task_routes.get('/get_task_by_id/{id}', response_model=OneTaskResponse, status_code=status.HTTP_200_OK)
def get_task_by_id(id: int , db: Session = Depends(get_db)):
    return controller.get_task_by_id(id , db)

@task_routes.put('/update_task/{id}', response_model=OneTaskResponse, status_code=status.HTTP_200_OK)
def update_task(id:int , body: TaskCreate , db: Session = Depends(get_db)):
    return controller.update_task(id , body , db)

@task_routes.delete('/delete_task/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id:int , db: Session = Depends(get_db)):
    return controller.delete_task(id , db)


@task_routes.put('/mark_task_as_completed/{id}', response_model=OneTaskResponse, status_code=status.HTTP_200_OK)
def mark_task_as_completed(id:int , db: Session = Depends(get_db)):
    return controller.mark_task_as_completed(id , db)
 
    