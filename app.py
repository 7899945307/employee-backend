from flask import Flask, jsonify
from flask_cors import CORS
import json
import urllib.request

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
        "name": "Liam Davis",
        "role": "Product Designer",
        "department": "Design",
        "email": "liam.davis@example.com",
        "location": "Mumbai",
    },
]


@app.get("/api/employees")
def get_employees():
    # #region debug-point A:backend-route
    urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:7777/event", data=json.dumps({"sessionId":"ui-not-working","runId":"pre-fix","hypothesisId":"A","location":"backend/app.py:get_employees","msg":"[DEBUG] backend employees route hit","data":{"count":len(EMPLOYEES)},"ts":0}).encode(), headers={"Content-Type":"application/json"})).read()
    # #endregion
    return jsonify(EMPLOYEES)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
