from fastapi import  APIRouter , Depends
from src.tasks import controller
from src.tasks.dtos import TaskCreate
from src.utils.db import get_db
task_routes = APIRouter(prefix='/tasks')

 
@task_routes.post('/create_task')
def create_task(body: TaskCreate , db = Depends(get_db)):
    return controller.create_task(body ,db)

@task_routes.get('/get_all_tasks')
def get_tasks(db = Depends(get_db)):
    return controller.get_tasks(db)

@task_routes.get('/get_task_by_id/{id}')
def get_task_by_id(id: int , db = Depends(get_db)):
    return controller.get_task_by_id(id , db)

@task_routes.put('/update_task/{id}')
def update_task(id:int , body: TaskCreate , db = Depends(get_db)):
    return controller.update_task(id , body , db)

@task_routes.delete('/delete_task/{id}')
def delete_task(id:int , db = Depends(get_db)):
    return controller.delete_task(id , db)


@task_routes.put('/mark_task_as_completed/{id}')
def mark_task_as_completed(id:int , db = Depends(get_db)):
    return controller.mark_task_as_completed(id , db)
 
    