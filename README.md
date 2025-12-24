# Fluid AI Task Board

Small, clean full-stack task board built for the Fluid AI Python Gen AI assignment.  
Backend is **FastAPI** (Python) with in-memory storage; frontend is a single **React + Tailwind (CDN)** page.  
The app includes a task board, progress insights, per-task time estimates, and a polished, mobile-friendly UI.

---

## Tech Stack

- **Backend**: FastAPI + Uvicorn, in-memory list of tasks
- **Frontend**: React 18 (UMD) + TailwindCSS from CDN, single `frontend/index.html`
- **Storage**: In-memory only (no external DB), reset on server restart

---

## How to Run Locally

### 1. Backend (FastAPI)

From the project root:

```bash
python -m venv .venv
.\.venv\Scripts\activate       # Windows PowerShell
pip install fastapi "uvicorn[standard]"

uvicorn backend.main:app --reload --port 8000
```

API base URL: `http://127.0.0.1:8000`

### 2. Frontend (React via CDN)

In a second terminal:

```bash
cd frontend
python -m http.server 5173
```

Open `http://127.0.0.1:5173/` in your browser.  
The frontend calls the API at `http://localhost:8000`.

---

## User Flow

### Task Board

The app opens directly on the **Vibe Task Board**:

- **Add task**
  - Title input
  - Time estimate: numeric value + unit dropdown (`sec`, `min`, `hrs`, `days`, `months`, `years`)
  - Priority dropdown: `Chill`, `Steady`, `Laser Focus`
  - **Add Task** button aligned on the left

- **Task list**
  - Each task row shows:
    - Title
    - Priority badge
    - Estimated time (value + unit)
    - Created at time
    - Checkbox to mark complete
    - **Delete** button

- **Per-task progress**
  - Under each task, a small progress bar shows `0%` when pending and `100%` when completed, with a matching percentage label.

### Insights / Unique Features

- **Momentum Pulse card**
  - Overall progress bar and percentage (completed tasks / total).
  - **Streak days**: how many consecutive days had at least one completed task.
  - **Suggestion**: highlights the oldest pending task ("Try finishing: <task> next.").

- **Serenity Mode card**
  - Explains the "mood" of the board (soft gradients, focused workflow).

- **Tasks card**
  - Header with **Tasks** label and hint text.
  - A second progress bar summarizing task completion right above the list.

The layout is responsive (single column on mobile, two columns on larger screens) and uses the Poppins font with a plum gradient background to match a modern product UI.

---

## API Endpoints

All endpoints operate on in-memory data.

- `GET /health`  
  ```json
  { "status": "ok" }
  ```

- `GET /tasks` → `List[Task]`  
  List all tasks, sorted by creation time.

- `POST /tasks` → `Task`  
  Body:
  ```json
  {
    "title": "string",
    "priority": "chill | normal | focus",
    "estimate_value": 30,
    "estimate_unit": "minutes"
  }
  ```

- `PATCH /tasks/{id}` → `Task`  
  Body:
  ```json
  { "completed": true }
  ```

- `DELETE /tasks/{id}`  
  Delete task by id.

- `GET /insights` → `Insight`  
  Returns:
  ```json
  {
    "total": 0,
    "completed": 0,
    "progress": 0.0,
    "streak_days": 0,
    "suggestion": "string"
  }
  ```

> All data is in memory; restarting the backend clears tasks and streaks.

---

## Unique Features That Stand Out

1. **Flexible Time Estimates**: Tasks can be estimated in seconds, minutes, hours, days, months, or years, making it easy to track both quick tasks and long-term projects.
2. **Per-Task Progress Bars**: Each task has its own visual progress indicator (0% → 100%) that updates when completed.
3. **Streak Tracking**: Automatically tracks consecutive days with completed tasks to maintain momentum.
4. **Smart Suggestions**: Backend suggests the oldest incomplete task to help prioritize work.
5. **Polished UI**: Gradient background, glassmorphism cards, and responsive design that works on mobile and desktop.

---

## Notes for Reviewers

- This repo contains only source code and assets; any prompt history from Cursor is **not** part of the repository.
- You can inspect the UI by opening `frontend/index.html` with any static server (e.g. `python -m http.server`) even without running the backend, though API-driven features will then return errors.
- For production, this design would be extended with:
  - Persistent DB (e.g. Postgres) for users and tasks.
  - Real auth (hashed passwords, sessions/JWTs).
  - Real email / notification service for reminders and confirmations.
