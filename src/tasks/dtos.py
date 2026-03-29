from asyncio import Task
from typing import Optional
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    is_completed: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool
    user_id : int | None = 0


class AllTasksResponse(BaseModel):
    status: str
    data: list[TaskResponse]


class OneTaskResponse(BaseModel):
    status: str
    data: TaskResponse