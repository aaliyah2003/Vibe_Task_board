# Replit Deployment Guide

## Quick Setup Steps

1. **Upload all files to Replit:**
   - Upload the entire project folder (including `backend/`, `frontend/`, `main.py`, `.replit`, `requirements.txt`)

2. **Replit will automatically:**
   - Install dependencies from `requirements.txt`
   - Run `main.py` (configured in `.replit`)

3. **The app structure:**
   - Backend API: Available at `/api/*` (e.g., `/api/tasks`, `/api/health`)
   - Frontend: Served at root `/` (shows `frontend/index.html`)
   - Frontend automatically detects Replit and uses `/api` instead of `localhost:8000`

4. **Check the Console:**
   - You should see: `INFO: Uvicorn running on http://0.0.0.0:8000`
   - If you see errors, check that all files are uploaded correctly

5. **Get your preview URL:**
   - Click the "Open in new tab" button in Replit's preview pane
   - Copy that URL - that's your preview link!

## Troubleshooting

- **If preview keeps loading:**
  - Check the Console tab for errors
  - Make sure `main.py` is in the root directory
  - Verify `frontend/index.html` exists
  - Check that `backend/main.py` exists

- **If API calls fail:**
  - Open browser DevTools (F12) → Console
  - Check if API calls are going to `/api/tasks` (correct) or `http://localhost:8000` (wrong)
  - The frontend should auto-detect Replit and use `/api`

- **Port issues:**
  - Replit uses the `PORT` environment variable automatically
  - The `main.py` reads this: `port = int(os.environ.get("PORT", 8000))`

## File Structure on Replit

```
/
├── main.py              # Entry point (serves both API + frontend)
├── .replit              # Replit configuration
├── requirements.txt     # Python dependencies
├── backend/
│   └── main.py         # FastAPI backend routes
└── frontend/
    └── index.html       # React frontend
```

