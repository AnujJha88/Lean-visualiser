# Lean Visualizer (V0)

> **"Cyberpunk Proof Assistant"** — Visualize Lean 4 proof states with an interactive, edgy timeline.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Frontend](https://img.shields.io/badge/frontend-Svelte%20%2B%20Vite-orange)
![Backend](https://img.shields.io/badge/backend-FastAPI%20%2B%20Python-green)
![Style](https://img.shields.io/badge/style-Cyberpunk-ff003c)

## 🔮 What is this?

**Lean Visualizer** is a modern, interactive debugging tool for the **Lean 4** theorem prover. It transforms the linear text of a proof into a **time-traveling visual experience**, allowing you to see exactly how the mathematical "state" evolves with every single keystroke and tactic.

Instead of reading a proof and mentally tracking hypothesis changes, you can:
*   **Scrub** back and forth through time (tactics).
*   **See** exactly when a goal is split, solved, or transformed.
*   **Debug** complex proofs (like Induction or Calc steps) by isolating each transformation.

It's wrapped in a **Cyberpunk / Terminal** aesthetic because verified mathematics is the closest thing we have to coding reality itself.

## ✨ Key Features

*   **Interactive Timeline Scrubbing**: Don't just read code. Play it. The timeline shows every tactic execution step.
*   **Deep State Inspection**: The right-hand panel shows the full proof context (hypotheses) and current goals (targets) for the selected step.
*   **Smart Diffing**: We calculate exactly what changed. New hypotheses glow **Cyan**; closed goals turn **Green**.
*   **Real-time Analysis**: Powered by `live.lean-lang.org`, ensuring 100% accurate Lean 4 verification.
*   **Included Examples**:
    *   **Logic Chains**: Visualizing constructive logic puzzles.
    *   **Induction**: Watching the base case and inductive step separate.
    *   **Calculation**: Seeing algebraic rewrites happen line-by-line.

## 🛠️ Tech Stack

This project uses a hybrid architecture to bridge web frontend with proof assistant backend:

*   **Frontend**: Built with **Svelte** and **Vite** for blazing fast reactivity. Uses **Monaco Editor** (the engine behind VS Code) for a native coding experience.
*   **Backend**: **FastAPI (Python)** server that acts as a bridge. It manages the **WebSocket** connection to the Lean server, parsing LSP (Language Server Protocol) messages into a structured timeline.
*   **Visuals**: Custom CSS variable system implementing scanlines, perspective grids, and neon glow effects without heavy UI libraries.

## 💻 Local Development

Want to hack on it?

### 1. Backend Setup
```bash
cd backend
python -m venv .venv
# Activate venv:
# Windows: .\.venv\Scripts\Activate.ps1
# Mac/Linux: source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Running
Open `http://localhost:5173`. The app will automatically proxy API requests to your local backend.

## 📄 License
MIT
