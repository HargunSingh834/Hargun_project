# Security Incident Reporting Portal

A lightweight web platform designed for employee security incident submission and real-time SOC triage tracking.

## Core Features
- **Employee Reporting Form**: Allows users to log security incidents with email, category, severity rating, and description.
- **Auto Reference Generation**: Generates unique tracking IDs (e.g., `INC-84920`) per incident.
- **SOC Triage Dashboard**: Displays active incidents organized by priority badge and timestamp.
- **SQLite Persistence**: Stores all reported incidents locally in `incidents.db`.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Portal
```bash
python app.py
```

### 3. Access in Browser
Open `http://localhost:5000` to submit reports and view the SOC Triage Dashboard.
