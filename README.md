# SomeoneElseAI

## Requirements

- Python 3.12.8
- Node.js (for frontend)

## Setup

### Backend

```bash
pyenv local 3.12.8
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Run

### Both Frontend and Backend (Recommended)

Run both services with a single command using the provided script:

```bash
./dev.sh
```

This will start:

- **Backend** on `http://localhost:8000`
- **Frontend** on `http://localhost:3000`

Press `Ctrl+C` to stop both services.

### Backend Only

```bash
source venv/bin/activate
uvicorn src.api.api:app --reload
```

Backend will be available at `http://localhost:8000`.

### Frontend Only

First, ensure the backend is running, then:

```bash
cd frontend
npm run dev
```

Frontend will be available at `http://localhost:3000` and will proxy `/healthz` requests to the backend at `http://localhost:8000`.

## Test

```bash
source venv/bin/activate
python -m pytest tests/test_api.py -v
```
