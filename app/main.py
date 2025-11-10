from fastapi import FastAPI
from app.routes import router  # <-- Import router from routes.py

app = FastAPI(
    title="Task Management System API",
    description="API for managing tasks",
    version="1.0"
)

# Register routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Task Manager API is running!"}
