# mirror

I believe that talking through your mental load will lighten it but the thought of sitting in a therapist's office is mad cringe. I also believe that Big AI/Venture Capitalists cannot and should not be trusted with your deepest thoughts, so I built this. If you're asking why *I* should be trusted with them, that's the right question. There's not really anything I can say to reassure you other than pointing out that I am too preoccupied with my own problems to intrude on yours.

Live site: [mirrorq.ai](https://mirrorq.ai) (Currently just static react, the model is too large for any free tier hosting, looking for workarounds rn)

## What this is

A React frontend talks to a Flask API that runs a local Mistral 7B model (via `ctransformers`). User messages go through tagging and moderation checks before the model responds. Chat history is stored per-username in `backend/data/` (gitignored).

## Prerequisites

- **Python 3.10+** (3.13 works on the maintainer's machine)
- **Node.js 18+** and npm
- **~8 GB RAM** free — the model is downloaded on first run (~4.4 GB) and loaded into memory
- **Git**

## Local setup

Clone the repo, then run the **backend** and **frontend** in two separate terminals.

### 1. Backend (Flask API — port 5000)

```bash
git clone https://github.com/VlllLE/mirror.git
cd mirror

python -m venv venv
```

Activate the virtual environment:

```bash
# Windows (Git Bash / CMD)
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

Install dependencies and start the server:

```bash
pip install -r backend/requirements.txt
cd backend
python app.py
```

On first start, the Mistral GGUF model is downloaded from Hugging Face. This can take a while. When ready, you should see:

```
 * Running on http://127.0.0.1:5000
```

Health check: [http://127.0.0.1:5000/health](http://127.0.0.1:5000/health) → `{"status":"ok"}`

### 2. Frontend (React — port 3000)

In a **second terminal**:

```bash
cd mirror/frontend
npm install
npm start
```

Opens [http://localhost:3000](http://localhost:3000). The app talks to the backend at `http://127.0.0.1:5000` by default — no env vars needed for local dev.

### 3. Use it

1. Pick a username (used to namespace chat memory)
2. Type a message and send
3. Watch the backend terminal for `🪞 Handling reflection for user: ...` to confirm the request landed

## Project layout

```
mirror/
├── backend/          Flask API, model, moderation/tag engines
│   ├── app.py        Main server
│   ├── data/         Per-user chat memory (created at runtime, not in git)
│   └── requirements.txt
├── frontend/         React app (Create React App)
│   ├── src/App.js
│   └── package.json
└── vercel.json       Frontend deploy config (Vercel)
```

## Optional environment variables

| Variable | Where | Default (local) | Purpose |
|----------|-------|-----------------|---------|
| `REACT_APP_API_URL` | frontend | `http://127.0.0.1:5000` | Backend URL (set in production) |
| `ALLOWED_ORIGINS` | backend | `http://localhost:3000` | CORS origins, comma-separated |
| `PORT` | backend | `5000` | Server port |
| `FLASK_DEBUG` | backend | off | Set to `1` to enable Flask debug mode |

## Running backend tests

```bash
cd backend
python test_tag_engine.py
```

Flag/moderation CLI:

```bash
cd backend
python flag_cli.py
```

## Troubleshooting

**Frontend loads but messages do nothing** — backend isn't running, or not on port 5000.

**Backend crashes on startup** — not enough RAM for the 7B model. Close other heavy apps or use a machine with more memory.

**`npm start` fails from repo root** — `package.json` lives in `frontend/`. Run npm commands from there.

**CORS errors in the browser** — if you're serving the frontend from a URL other than `localhost:3000`, set `ALLOWED_ORIGINS` on the backend to match.

## Production

Frontend is on Vercel ([mirrorq.ai](https://mirrorq.ai)). The backend needs a host with ~8 GB RAM (e.g. Railway) — it won't run on Vercel. Am working on getting backend live as well. You can send me money to assist with this.

## Contact m@vile.cx

