from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from app.models import Task, TaskUpdate
from app.utils.file_utils import load_data, save_data

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to the Task Management System API!"}

@router.get("/about")
def read_about():
    return {"message": "An API that lets you create, view, update, and delete tasks."}

@router.get("/tasks")
def view_all_tasks():
    return load_data()

@router.get("/task/{task_id}")
def view_task(task_id: str = Path(..., description="ID of the task", example="T001")):
    data = load_data()
    if task_id in data:
        return data[task_id]
    raise HTTPException(status_code=404, detail="Task not found")

@router.get("/sort")
def sort_tasks(
    sort_by: str = Query(..., description="Sort by estimated_hours, hours_spent, or progress"),
    order: str = Query("asc", description="Sort order: 'asc' or 'desc'")
):
    valid_fields = ["estimated_hours", "hours_spent", "progress"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Choose from {valid_fields}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Use 'asc' or 'desc'")

    data = load_data()
    reverse = order == "desc"
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=reverse)
    return sorted_data

@router.post("/create")
def create_task(task: Task):
    data = load_data()
    if task.id in data:
        raise HTTPException(status_code=400, detail="Task already exists")
    data[task.id] = task.model_dump(exclude={"id"})
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Task created successfully"})

@router.put("/edit/{task_id}")
def update_task(task_id: str, task_update: TaskUpdate):
    data = load_data()
    if task_id not in data:
        raise HTTPException(status_code=404, detail="Task not found")

    existing_task = data[task_id]
    updated_fields = task_update.model_dump(exclude_unset=True)
    for key, value in updated_fields.items():
        existing_task[key] = value

    existing_task["id"] = task_id
    updated_task = Task(**existing_task)

    data[task_id] = updated_task.model_dump(exclude={"id"})
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Task updated successfully"})

@router.delete("/delete/{task_id}")
def delete_task(task_id: str):
    data = load_data()
    if task_id not in data:
        raise HTTPException(status_code=404, detail="Task not found")

    del data[task_id]
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Task deleted successfully"})
