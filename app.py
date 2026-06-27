from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
import urllib.request

app = Flask(__name__)
CORS(app)

# #region debug-point A:report-helper
def _debug_report(hypothesis_id, location, msg, data):
    try:
        urllib.request.urlopen(
            urllib.request.Request(
                "http://127.0.0.1:7778/event",
                data=json.dumps(
                    {
                        "sessionId": "nixpacks-start-command",
                        "runId": "pre-fix",
                        "hypothesisId": hypothesis_id,
                        "location": location,
                        "msg": msg,
                        "data": data,
                    }
                ).encode(),
                headers={"Content-Type": "application/json"},
            )
        ).read()
    except Exception:
        pass


_debug_report(
    "A",
    "backend/app.py:module-load",
    "[DEBUG] backend module loaded",
    {"port_env": os.getenv("PORT"), "cwd": os.getcwd()},
)
# #endregion

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
    # #region debug-point B:route-hit
    _debug_report(
        "B",
        "backend/app.py:get_employees",
        "[DEBUG] backend employees route hit",
        {"count": len(EMPLOYEES)},
    )
    # #endregion
    return jsonify(EMPLOYEES)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "4000")))
