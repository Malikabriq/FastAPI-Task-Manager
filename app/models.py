from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

class Task(BaseModel):
    id: Annotated[str, Field(..., description="Unique ID of the task", examples=["T001"])]
    title: Annotated[str, Field(..., description="Title of the task")]
    description: Annotated[str, Field(..., description="Detailed description of the task")]
    priority: Annotated[Literal['low', 'medium', 'high'], Field(..., description="Priority of the task")]
    status: Annotated[Literal['pending', 'in_progress', 'completed'], Field(..., description="Current status of the task")]
    estimated_hours: Annotated[float, Field(..., gt=0, description="Estimated time to complete the task (in hours)")]
    hours_spent: Annotated[float, Field(..., ge=0, description="Hours spent on the task so far")]

    @computed_field
    @property
    def progress(self) -> float:
        """Calculated completion percentage."""
        return round((self.hours_spent / self.estimated_hours) * 100, 2) if self.estimated_hours else 0.0

    @computed_field
    @property
    def verdict(self) -> str:
        """Verdict based on progress."""
        if self.progress == 100:
            return "Task Completed"
        elif self.progress >= 70:
            return "Almost Done"
        elif self.progress >= 30:
            return "In Progress"
        else:
            return "Just Started"

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Literal['low', 'medium', 'high']] = None
    status: Optional[Literal['pending', 'in_progress', 'completed']] = None
    estimated_hours: Optional[float] = Field(default=None, gt=0)
    hours_spent: Optional[float] = Field(default=None, ge=0)
