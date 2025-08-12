from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Mock user database
users = {
    "test@example.com": {
        "password": "1234",
        "allowed_apps": ["notepad.exe", "calc.exe"],
        "session_minutes": 1
    }
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if email in users and users[email]["password"] == password:
        now = datetime.now()
        start_time = now.isoformat()
        end_time = (now + timedelta(minutes=users[email]["session_minutes"])).isoformat()

        return jsonify({
            "token": "mock_token_123",
            "session_start": start_time,
            "session_end": end_time,
            "allowed_apps": users[email]["allowed_apps"]
        })
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route('/session', methods=['GET'])
def session():
    token = request.headers.get("Authorization")
    if token == "Bearer mock_token_123":
        return jsonify({
            "status": "active"
        })
    return jsonify({"status": "inactive"}), 403


if __name__ == '__main__':
    app.run(debug=True)
