# Lean Visualizer Backend

Python backend for the Lean Proof Visualizer.

## Setup

```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Run

```powershell
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `POST /api/proof/analyze` - Analyze Lean proof

## Development

API docs available at: http://localhost:8000/docs
