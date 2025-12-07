# SomeoneElseAI

## Requirements

- Python 3.12.8

## Setup

```bash
pyenv local 3.12.8
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
source venv/bin/activate
uvicorn src.api.api:app --reload
```

## Test

```bash
source venv/bin/activate
python -m pytest tests/test_api.py -v
```
