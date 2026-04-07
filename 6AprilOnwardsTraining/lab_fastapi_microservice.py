"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         HANDS-ON LAB: Build a Task Management Microservice                 ║
║         Copilot-Assisted FastAPI Development                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

GOAL
────
Build a fully working REST API for task management using FastAPI and GitHub
Copilot. By the end of this lab you will have:

  • A structured Python microservice (models / service / router layers)
  • Five RESTful endpoints (CRUD for tasks)
  • Auto-generated OpenAPI documentation at /docs
  • Centralised configuration using Pydantic BaseSettings

HOW TO USE COPILOT
──────────────────
1. Read each TODO block carefully.
2. Write a descriptive comment above the TODO (describe WHAT, not HOW).
3. Pause for 2 seconds — Copilot will suggest a completion.
4. Press Tab to accept, or use Alt+] / Alt+[ to cycle suggestions.
5. Always review what Copilot generated before moving on.

SETUP
─────
  pip install fastapi uvicorn pydantic

RUN THE APP
───────────
  uvicorn lab_fastapi_microservice:app --reload

OPEN THE DOCS
─────────────
  http://127.0.0.1:8000/docs   ← Swagger UI (interactive)
  http://127.0.0.1:8000/redoc  ← ReDoc (readable)
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: IMPORTS
# Import FastAPI, HTTPException, status codes, Pydantic BaseModel, Optional,
# List, datetime, and uuid4 from the standard library.
# ─────────────────────────────────────────────────────────────────────────────

# TODO 1: Add all required imports below this comment.
# Hint: You need fastapi, pydantic, typing, datetime, and uuid modules.

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: CONFIGURATION
# Centralise app settings using a simple class (or Pydantic BaseSettings).
# ─────────────────────────────────────────────────────────────────────────────

# TODO 2: Create a Settings class with:
#   - app_name: str  (default: "Task Service")
#   - version: str   (default: "1.0.0")
#   - debug: bool    (default: False)
#   - max_tasks: int (default: 100)
# Then create a settings = Settings() instance.

class Settings(BaseModel):
    app_name: str = "Task Service"
    version: str = "1.0.0"
    debug: bool = False
    max_tasks: int = 100

settings = Settings()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: PYDANTIC MODELS (Data Schemas)
# Define the data shapes for our Task resource.
# ─────────────────────────────────────────────────────────────────────────────

# TODO 3: Create a TaskStatus enum with values: PENDING, IN_PROGRESS, DONE
# Hint: use Python's enum.Enum class

from enum import Enum

# Write a comment describing the TaskStatus enum, then let Copilot complete it:
# Enum for task lifecycle states: pending → in_progress → done

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


# TODO 4: Create a TaskCreate model (used for POST requests) with:
#   - title: str       (required, min length 1, max length 200)
#   - description: Optional[str]
#   - status: TaskStatus  (default: PENDING)

# Pydantic model for creating a new task — used in POST /tasks request body.
# title is required; description is optional; status defaults to PENDING.

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, description="Optional task description")
    status: TaskStatus = Field(TaskStatus.PENDING, description="Task lifecycle status")


# TODO 5: Create a TaskUpdate model (used for PATCH requests) with all optional fields:
#   - title: Optional[str]
#   - description: Optional[str]
#   - status: Optional[TaskStatus]

# Pydantic model for updating an existing task — all fields are optional (partial update).

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


# TODO 6: Create a Task response model (returned to clients) that extends TaskCreate with:
#   - id: UUID         (auto-generated)
#   - created_at: datetime
#   - updated_at: datetime

# Full Task response model — includes server-generated id and timestamps.

class Task(TaskCreate):
    id: UUID = Field(default_factory=uuid4, description="Unique task identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {UUID: str}


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: SERVICE LAYER (Business Logic)
# Keep all business logic here — no HTTP/FastAPI imports in this layer.
# ─────────────────────────────────────────────────────────────────────────────

class TaskService:
    """Service layer for Task CRUD operations.

    Uses an in-memory store for simplicity. In production this would
    talk to a database via a repository layer.
    """

    def __init__(self) -> None:
        # In-memory storage: dict[UUID → Task]
        self._store: dict[str, Task] = {}

    # TODO 7: Implement get_all() → returns a List[Task] of all tasks.
    # Return all tasks from the in-memory store as a list.

    def get_all(self) -> List[Task]:
        return list(self._store.values())

    # TODO 8: Implement get_by_id(task_id: UUID) → returns Optional[Task].
    # Look up a task by its UUID string key. Return None if not found.

    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        return self._store.get(str(task_id))

    # TODO 9: Implement create(data: TaskCreate) → returns Task.
    # Build a new Task from TaskCreate data, store it, and return it.
    # Raise a ValueError if the store already contains max_tasks entries.

    def create(self, data: TaskCreate) -> Task:
        if len(self._store) >= settings.max_tasks:
            raise ValueError(f"Task limit of {settings.max_tasks} reached")
        task = Task(**data.model_dump())
        self._store[str(task.id)] = task
        return task

    # TODO 10: Implement update(task_id: UUID, data: TaskUpdate) → returns Optional[Task].
    # Apply only the non-None fields from TaskUpdate. Update updated_at. Return None if not found.

    def update(self, task_id: UUID, data: TaskUpdate) -> Optional[Task]:
        task = self.get_by_id(task_id)
        if not task:
            return None
        update_data = data.model_dump(exclude_none=True)
        updated = task.model_copy(update={**update_data, "updated_at": datetime.utcnow()})
        self._store[str(task_id)] = updated
        return updated

    # TODO 11: Implement delete(task_id: UUID) → returns bool.
    # Remove a task from the store. Return True if deleted, False if not found.

    def delete(self, task_id: UUID) -> bool:
        key = str(task_id)
        if key not in self._store:
            return False
        del self._store[key]
        return True


# Singleton service instance (in production, use dependency injection)
task_service = TaskService()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: FASTAPI APP & ENDPOINTS (Router Layer)
# ─────────────────────────────────────────────────────────────────────────────

# TODO 12: Create the FastAPI app instance.
# Use settings.app_name as the title, settings.version as the version,
# and add a description explaining it is a task management microservice.

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="A modular Task Management REST API built with FastAPI and Copilot-assisted development.",
)


# ── Health Check ──────────────────────────────────────────────────────────────

# TODO 13: Create a GET /health endpoint that returns app status.
# Return: {"status": "ok", "app": app name, "version": version, "timestamp": now}

@app.get("/health", tags=["Meta"])
async def health_check():
    """Returns service health status and metadata."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.version,
        "timestamp": datetime.utcnow().isoformat(),
    }


# ── List Tasks ────────────────────────────────────────────────────────────────

# TODO 14: Create GET /tasks endpoint that returns all tasks.
# Response type: List[Task]. Tag: "Tasks".

@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
async def list_tasks() -> List[Task]:
    """Retrieve all tasks."""
    return task_service.get_all()


# ── Get Single Task ───────────────────────────────────────────────────────────

# TODO 15: Create GET /tasks/{task_id} endpoint.
# Return the task if found. Raise HTTP 404 with detail "Task not found" if missing.

@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def get_task(task_id: UUID) -> Task:
    """Retrieve a single task by ID. Returns 404 if not found."""
    task = task_service.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


# ── Create Task ───────────────────────────────────────────────────────────────

# TODO 16: Create POST /tasks endpoint.
# Accept a TaskCreate body. Return the created Task with status 201 Created.
# Catch ValueError from the service and raise HTTP 400.

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(data: TaskCreate) -> Task:
    """Create a new task. Returns 400 if task limit is reached."""
    try:
        return task_service.create(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ── Update Task ───────────────────────────────────────────────────────────────

# TODO 17: Create PATCH /tasks/{task_id} endpoint for partial updates.
# Accept a TaskUpdate body. Return the updated Task or raise 404.

@app.patch("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def update_task(task_id: UUID, data: TaskUpdate) -> Task:
    """Partially update a task. Raises 404 if the task does not exist."""
    updated = task_service.update(task_id, data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return updated


# ── Delete Task ───────────────────────────────────────────────────────────────

# TODO 18: Create DELETE /tasks/{task_id} endpoint.
# Return 204 No Content on success. Raise 404 if task does not exist.

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_task(task_id: UUID) -> None:
    """Delete a task by ID. Returns 204 on success, 404 if not found."""
    if not task_service.delete(task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: STRETCH GOALS
# Complete these if you finish early, or explore at home.
# ─────────────────────────────────────────────────────────────────────────────

# STRETCH 1: Add a GET /tasks?status=pending filter endpoint
# Let Copilot generate a filtered version of list_tasks():
# # GET /tasks with optional status query parameter for filtering

# STRETCH 2: Add a bulk-create endpoint
# # POST /tasks/bulk — accept a list of TaskCreate objects, return a list of created Tasks

# STRETCH 3: Write a test using FastAPI's TestClient
# # Test: POST /tasks creates a task and returns 201 with the task body
# from fastapi.testclient import TestClient
# client = TestClient(app)
# def test_create_task():
#     ...  # Let Copilot complete this

# STRETCH 4: Add a statistics endpoint
# # GET /stats — return total tasks, counts by status, oldest and newest task dates


# ─────────────────────────────────────────────────────────────────────────────
# ENTRYPOINT (for running directly with `python lab_fastapi_microservice.py`)
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("lab_fastapi_microservice:app", host="127.0.0.1", port=8000, reload=True)
