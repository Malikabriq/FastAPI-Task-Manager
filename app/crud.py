from .db import load_data, save_data
from .models import Task, TaskUpdate


def get_all():
    return load_data()


def get(task_id: str):
    data = load_data()
    return data.get(task_id)


def create(task: Task):
    data = load_data()
    if task.id in data:
        raise ValueError("Task already exists")
    data[task.id] = task.model_dump(exclude={"id"})
    save_data(data)

def update(task_id: str, task_update: TaskUpdate):
    data = load_data()
    if task_id not in data:
        raise ValueError("Task not found")
    
    existing_task = data[task_id]
    updated_fields = task_update.model_dump(exclude_unset=True)

    for key, value in updated_fields.items():
        existing_task[key] = value

    existing_task["id"] = task_id
    updated_task = Task(**existing_task)
    data[task_id] = updated_task.model_dump(exclude={"id"})
    save_data(data)


def delete(task_id: str):
    data = load_data()
    if task_id not in data:
        raise ValueError("Task not found")
    del data[task_id]
    save_data(data)
