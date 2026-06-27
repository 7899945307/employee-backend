# Employee Backend

Python backend API built with Flask. It returns a list of employees for the React frontend.

## Run locally

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://username:password@host:5432/database_name
python app.py
```

The API runs on `http://localhost:4000`.

## API routes

- `GET /api/employees`
- `GET /api/employees/:id`
- `POST /api/employees`
- `PUT /api/employees/:id`
- `DELETE /api/employees/:id`

## Database

- Backend reads employees from Postgres using `DATABASE_URL`
- On startup it creates the `employees` table if it does not exist
- It also seeds the table with the current sample employee data
- Connection is configured to work with PgBouncer-style pooled Postgres connections

## GitHub push

```bash
git init
git add .
git commit -m "Initial backend commit"
git branch -M main
git remote add origin <your-backend-repo-url>
git push -u origin main
```
