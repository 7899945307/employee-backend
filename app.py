import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from psycopg import connect
from psycopg.rows import dict_row

app = Flask(__name__)
CORS(app)

SEED_EMPLOYEES = [
    {
        "name": "Ava Johnson",
        "role": "Frontend Developer",
        "department": "Engineering",
        "email": "ava.johnson@example.com",
        "location": "Bengaluru",
    },
    {
        "name": "Noah Smith",
        "role": "Backend Developer",
        "department": "Engineering",
        "email": "noah.smith@example.com",
        "location": "Pune",
    },
    {
        "name": "Emma Brown",
        "role": "HR Manager",
        "department": "People Operations",
        "email": "emma.brown@example.com",
        "location": "Hyderabad",
    },
    {
        "name": "manish kulkarni developer thunnya",
        "role": "Product Designer",
        "department": "Design",
        "email": "liam.davis@example.com",
        "location": "Mumbai",
    },
]


def get_database_url():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is required.")
    return database_url


def get_connection():
    return connect(get_database_url(), row_factory=dict_row, prepare_threshold=None)


def init_db():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS employees (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    department TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    location TEXT NOT NULL
                )
                """
            )

            cursor.executemany(
                """
                INSERT INTO employees (name, role, department, email, location)
                VALUES (%(name)s, %(role)s, %(department)s, %(email)s, %(location)s)
                ON CONFLICT (email) DO UPDATE SET
                    name = EXCLUDED.name,
                    role = EXCLUDED.role,
                    department = EXCLUDED.department,
                    location = EXCLUDED.location
                """,
                SEED_EMPLOYEES,
            )


def fetch_employees():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, role, department, email, location
                FROM employees
                ORDER BY id
                """
            )
            return cursor.fetchall()


def fetch_employee(employee_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, role, department, email, location
                FROM employees
                WHERE id = %s
                """,
                (employee_id,),
            )
            return cursor.fetchone()


def validate_employee_payload(payload):
    required_fields = ["name", "role", "department", "email", "location"]
    missing_fields = [field for field in required_fields if not str(payload.get(field, "")).strip()]
    if missing_fields:
        return {"error": f"Missing required fields: {', '.join(missing_fields)}"}
    return None


@app.get("/api/employees")
def get_employees():
    return jsonify(fetch_employees())


@app.get("/api/employees/<int:employee_id>")
def get_employee(employee_id):
    employee = fetch_employee(employee_id)
    if not employee:
        return jsonify({"error": "Employee not found."}), 404
    return jsonify(employee)


@app.post("/api/employees")
def create_employee():
    payload = request.get_json(silent=True) or {}
    validation_error = validate_employee_payload(payload)
    if validation_error:
        return jsonify(validation_error), 400

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO employees (name, role, department, email, location)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, name, role, department, email, location
                """,
                (
                    payload["name"].strip(),
                    payload["role"].strip(),
                    payload["department"].strip(),
                    payload["email"].strip(),
                    payload["location"].strip(),
                ),
            )
            employee = cursor.fetchone()
        connection.commit()

    return jsonify(employee), 201


@app.put("/api/employees/<int:employee_id>")
def update_employee(employee_id):
    payload = request.get_json(silent=True) or {}
    validation_error = validate_employee_payload(payload)
    if validation_error:
        return jsonify(validation_error), 400

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE employees
                SET name = %s,
                    role = %s,
                    department = %s,
                    email = %s,
                    location = %s
                WHERE id = %s
                RETURNING id, name, role, department, email, location
                """,
                (
                    payload["name"].strip(),
                    payload["role"].strip(),
                    payload["department"].strip(),
                    payload["email"].strip(),
                    payload["location"].strip(),
                    employee_id,
                ),
            )
            employee = cursor.fetchone()
        connection.commit()

    if not employee:
        return jsonify({"error": "Employee not found."}), 404

    return jsonify(employee)


@app.delete("/api/employees/<int:employee_id>")
def delete_employee(employee_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM employees
                WHERE id = %s
                RETURNING id
                """,
                (employee_id,),
            )
            deleted = cursor.fetchone()
        connection.commit()

    if not deleted:
        return jsonify({"error": "Employee not found."}), 404

    return jsonify({"message": "Employee deleted successfully.", "id": employee_id})


init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "4000")))
