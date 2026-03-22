from asyncio import Task

from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    is_completed: bool = False



class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool


class AllTasksResponse(BaseModel):
    status: str
    data: list[TaskResponse]


class OneTaskResponse(BaseModel):
    status: str
    data: TaskResponse