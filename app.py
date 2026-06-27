from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

EMPLOYEES = [
    {
        "id": 1,
        "name": "Ava Johnson",
        "role": "Frontend Developer",
        "department": "Engineering",
        "email": "ava.johnson@example.com",
        "location": "Bengaluru",
    },
    {
        "id": 2,
        "name": "Noah Smith",
        "role": "Backend Developer",
        "department": "Engineering",
        "email": "noah.smith@example.com",
        "location": "Pune",
    },
    {
        "id": 3,
        "name": "Emma Brown",
        "role": "HR Manager",
        "department": "People Operations",
        "email": "emma.brown@example.com",
        "location": "Hyderabad",
    },
    {
        "id": 4,
        "name": "manish kulkarni developer thunnya",
        "role": "Product Designer",
        "department": "Design",
        "email": "liam.davis@example.com",
        "location": "Mumbai",
    },
]


@app.get("/api/employees")
def get_employees():
    return jsonify(EMPLOYEES)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "4000")))
