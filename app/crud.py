from .db import load_data, save_data
from .models import Task

def get_all():
    return load_data()

def get(task_id):
    data = load_data()
    return data.get(task_id)

def create(task: Task):
    data = load_data()
    if task.id in data:
        raise ValueError("Already exists")
    data[task.id] = task.model_dump(exclude={"id"})
    save_data(data)

# update/delete similarly...
