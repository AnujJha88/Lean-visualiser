# Lean Proof Visualizer

A web app that visualizes Lean 4 proof state evolution with an interactive timeline.

## Features

- 📝 **Monaco Editor** - Write Lean 4 code with syntax highlighting
- ⏱️ **Proof Timeline** - Scrub through each tactic step
- 🔍 **State Display** - See goals and hypotheses at each step
- 🎨 **Diff Highlighting** - Spot what changed between steps

## Architecture

```
Frontend (Svelte)  →  Backend (FastAPI)  →  Lean4Web API
```

## Getting Started

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Development

- Backend runs on: http://localhost:8000
- Frontend runs on: http://localhost:5173
- API docs: http://localhost:8000/docs

## License

MIT
