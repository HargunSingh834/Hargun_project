import sqlite3
import datetime
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)
DB_FILE = "incidents.db"

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_ref TEXT NOT NULL,
            reporter_email TEXT NOT NULL,
            category TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'NEW',
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# HTML Template (Reporting Form + SOC Triage Dashboard)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Security Incident Reporting Portal</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 40px; background-color: #0f172a; color: #f8fafc; }
        .container { max-width: 900px; margin: 0 auto; }
        .card { background-color: #1e293b; padding: 24px; border-radius: 10px; margin-bottom: 24px; border: 1px solid #334155; }
        h1, h2 { color: #38bdf8; }
        label { display: block; margin-top: 10px; font-weight: bold; }
        input, select, textarea { width: 100%; padding: 10px; margin-top: 5px; border-radius: 6px; border: 1px solid #475569; background-color: #0f172a; color: white; box-sizing: border-box; }
        button { background-color: #0284c7; color: white; border: none; padding: 12px 20px; border-radius: 6px; margin-top: 15px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #0369a1; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #334155; padding: 12px; text-align: left; }
        th { background-color: #0f172a; color: #38bdf8; }
        .badge { padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85em; }
        .CRITICAL { background-color: #ef4444; color: white; }
        .HIGH { background-color: #f97316; color: white; }
        .MEDIUM { background-color: #eab308; color: black; }
        .LOW { background-color: #22c55e; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Security Incident Reporting Portal</h1>

        <!-- Form for Employees to Report Incidents -->
        <div class="card">
            <h2>Report a Security Incident</h2>
            <form action="/report" method="POST">
                <label>Your Email Address:</label>
                <input type="email" name="email" required placeholder="user@company.com">

                <label>Incident Category:</label>
                <select name="category">
                    <option value="Phishing Email">Phishing Email / Suspicious Link</option>
                    <option value="Lost / Stolen Device">Lost / Stolen Laptop or Mobile</option>
                    <option value="Unauthorized Access">Unauthorized Account Access</option>
                    <option value="Data Leak">Accidental Data Leak / Confidentiality Exposure</option>
                    <option value="Malware Infection">Malware / Ransomware Suspicion</option>
                    <option value="Other">Other Security Concern</option>
                </select>

                <label>Perceived Severity:</label>
                <select name="severity">
                    <option value="LOW">Low - Minimal Risk / Inquiry</option>
                    <option value="MEDIUM">Medium - Single Account / Non-Critical Device</option>
                    <option value="HIGH">High - Compromised Credentials / Active Malware</option>
                    <option value="CRITICAL">Critical - Data Breach / System-Wide Outage</option>
                </select>

                <label>Detailed Description:</label>
                <textarea name="description" rows="4" required placeholder="Describe what happened, including any URLs, filenames, or suspicious activities..."></textarea>

                <button type="submit">Submit Security Report</button>
            </form>
        </div>

        <!-- SOC Dashboard View -->
        <div class="card">
            <h2>SOC Incident Triage Dashboard</h2>
            <table>
                <thead>
                    <tr>
                        <th>Ref ID</th>
                        <th>Reporter</th>
                        <th>Category</th>
                        <th>Severity</th>
                        <th>Status</th>
                        <th>Submitted At</th>
                    </tr>
                </thead>
                <tbody>
                    {% for inc in incidents %}
                    <tr>
                        <td><strong>{{ inc[1] }}</strong></td>
                        <td>{{ inc[2] }}</td>
                        <td>{{ inc[3] }}</td>
                        <td><span class="badge {{ inc[4] }}">{{ inc[4] }}</span></td>
                        <td><code>{{ inc[6] }}</code></td>
                        <td>{{ inc[7] }}</td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="6" style="text-align: center; color: #94a3b8;">No security incidents reported yet.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents ORDER BY id DESC")
    incidents = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, incidents=incidents)

@app.route('/report', methods=['POST'])
def report():
    email = request.form.get('email')
    category = request.form.get('category')
    severity = request.form.get('severity')
    description = request.form.get('description')
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ref_id = f"INC-{int(datetime.datetime.now().timestamp()) % 100000}"

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO incidents (incident_ref, reporter_email, category, severity, description, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (ref_id, email, category, severity, description, timestamp))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🚀 Starting Security Incident Reporting Portal on http://localhost:5000")
    app.run(port=5000, debug=True)
