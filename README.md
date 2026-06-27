# Employee Backend

Python backend API built with Flask. It returns a list of employees for the React frontend.

## Run locally

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The API runs on `http://localhost:4000`.

## API routes

- `GET /api/employees`

## GitHub push

```bash
git init
git add .
git commit -m "Initial backend commit"
git branch -M main
git remote add origin <your-backend-repo-url>
git push -u origin main
```
