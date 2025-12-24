from datetime import date, datetime
from typing import List, Optional, Set
import os
import smtplib
import uuid

from email.message import EmailMessage
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    priority: Optional[str] = "normal"
    estimate_value: Optional[int] = None
    estimate_unit: Optional[str] = None


class TaskToggle(BaseModel):
    completed: bool


class Task(BaseModel):
    id: str
    title: str
    completed: bool = False
    priority: str = "normal"
    estimate_value: Optional[int] = None
    estimate_unit: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class Insight(BaseModel):
    total: int
    completed: int
    progress: float
    streak_days: int
    suggestion: Optional[str] = None


class EmailRequest(BaseModel):
    email: str


app = FastAPI(title="Task Board API", version="1.0.0")

# Simple in-memory storage
tasks: List[Task] = []
# Use typing.Set for Python 3.7 compatibility
completion_days: Set[date] = set()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _compute_streak() -> int:
    if not completion_days:
        return 0
    today = date.today()
    streak = 0
    cursor = today
    while cursor in completion_days:
        streak += 1
        cursor = date.fromordinal(cursor.toordinal() - 1)
    return streak


def _oldest_incomplete_title() -> Optional[str]:
    pending = [t for t in tasks if not t.completed]
    if not pending:
        return None
    pending.sort(key=lambda t: t.created_at)
    return pending[0].title


def _send_gmail_confirmation(recipient: str) -> None:
    """Send a simple confirmation email using Gmail SMTP.

    Requires GMAIL_USER and GMAIL_APP_PASSWORD environment variables to be set.
    """
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_password:
        raise HTTPException(
            status_code=500,
            detail="Email is not configured on the server. Set GMAIL_USER and GMAIL_APP_PASSWORD.",
        )

    msg = EmailMessage()
    msg["Subject"] = "Confirm your Fluid Task Board account"
    msg["From"] = gmail_user
    msg["To"] = recipient
    msg.set_content(
        "Thanks for creating your account on Fluid Task Board.\n\n"
        "Click the confirm button in the app to finish verification.\n\n"
        "This message was sent from your local assignment app."
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(gmail_user, gmail_password)
            smtp.send_message(msg)
    except Exception as exc:  # pragma: no cover - depends on network
        raise HTTPException(status_code=502, detail=f"Failed to send email: {exc}")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=List[Task])
def list_tasks():
    return sorted(tasks, key=lambda t: t.created_at)


@app.post("/tasks", response_model=Task, status_code=201)
def add_task(payload: TaskCreate):
    task = Task(
        id=str(uuid.uuid4()),
        title=payload.title.strip(),
        priority=(payload.priority or "normal"),
        estimate_value=payload.estimate_value,
        estimate_unit=payload.estimate_unit,
        created_at=datetime.utcnow(),
    )
    tasks.append(task)
    return task


@app.patch("/tasks/{task_id}", response_model=Task)
def toggle_task(task_id: str, payload: TaskToggle):
    for task in tasks:
        if task.id == task_id:
            task.completed = payload.completed
            task.completed_at = datetime.utcnow() if payload.completed else None
            task_day = date.today()
            if payload.completed:
                completion_days.add(task_day)
            else:
                completion_days.discard(task_day)
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    global tasks
    before = len(tasks)
    tasks = [t for t in tasks if t.id != task_id]
    if len(tasks) == before:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


@app.get("/insights", response_model=Insight)
def insights():
    total = len(tasks)
    completed = len([t for t in tasks if t.completed])
    progress = round((completed / total * 100) if total else 0.0, 2)
    streak = _compute_streak()
    suggestion = _oldest_incomplete_title()
    if suggestion:
        suggestion = f"Try finishing: “{suggestion}” next."
    else:
        suggestion = "All clear! Add something new to keep momentum."
    return Insight(
        total=total,
        completed=completed,
        progress=progress,
        streak_days=streak,
        suggestion=suggestion,
    )


@app.post("/send-confirmation")
def send_confirmation(payload: EmailRequest):
    """Trigger a confirmation email to the provided address."""
    _send_gmail_confirmation(payload.email)
    return {"ok": True}
