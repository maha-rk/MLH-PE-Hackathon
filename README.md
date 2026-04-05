MLH PE Hackathon — URL Shortener and Incident Response Platform
This project implements a production‑grade URL Shortener using Flask and Peewee ORM, combined with a complete Incident Response (IR) and Documentation suite.
It includes:

REST API for Users, URLs, and Events
URL creation, listing, updating, deletion, and redirect service
Users CRUD with CSV bulk import
Event logging with filtering and merging
Prometheus metrics exporter
Grafana Golden Signals dashboard
Alerting via email
Full documentation including runbooks and RCA


Features
URL Shortener

Create short URLs with collision‑safe generation
Redirect via /r/<shortcode>
Update URL metadata
Enable/disable URLs
Deduplicate URLs for each user
Filter URLs (?user_id=, ?is_active=)

Users API

Create users
List all users
Retrieve a user by ID
Update user details
Delete a user
CSV bulk import (POST /users/bulk)

Events API

Log creation and update events
Manual event creation
Filtering by URL, user, or event type
Advanced event merging logic


Installation
Install dependencies:
Shelluv syncShow more lines
Run the server:
Shelluv run python run.py``Show more lines
Health check:
Shellcurl http://localhost:5003/healthShow more lines

API Documentation
Users API
POST    /users
GET     /users
GET     /users/<id>
PUT     /users/<id>
DELETE  /users/<id>
POST    /users/bulk

URLs API
POST    /urls
GET     /urls
GET     /urls?user_id=<id>&is_active=<bool>
GET     /urls/<id>
PUT     /urls/<id>
DELETE  /urls/<id>
GET     /urls/<shortcode>/redirect

Events API
POST    /events
GET     /events

Full API documentation is available in docs/API.md.

Metrics (Prometheus)
Metrics endpoint:
/prom_metrics

Exports:

flask_app_total_requests
flask_app_avg_latency_ms
flask_app_error_count
CPU and memory usage


Grafana Dashboard
The Golden Signals dashboard includes:

Request volume
Average latency
Error count
Error rate
CPU usage
Memory usage

Screenshot available in screenshots/dashboard.png.

Incident Response Documentation
Runbook
Located in docs/RUNBOOK.md.
Includes:

Service downtime procedures
Error spike handling
Latency debugging
Redirect failures
Database issues
Recovery workflows

Root Cause Analysis (RCA)
Located in docs/RCA.md.

Architecture Diagram
              ┌──────────────────┐
              │     Frontend     │
              └──────────┬───────┘
                         │ HTTP
               ┌─────────▼────────┐
               │     Flask API     │
               │ /users, /urls,    │
               │ /events, /r/<id>  │
               └─────────┬────────┘
                         │ Peewee ORM
               ┌─────────▼────────┐
               │    SQLite DB      │
               └─────────┬────────┘
                         │ Metrics
               ┌─────────▼────────┐
               │    Prometheus     │
               └─────────┬────────┘
                         │
               ┌─────────▼────────┐
               │     Grafana       │
               └───────────────────┘


Tech Stack

Python 3.13
Flask
Peewee ORM
SQLite
Prometheus
Grafana
uv package manager
Docker Compose


Project Structure
MLH-PE-Hackathon/
│── app/
│── monitoring/
│── docs/
│── screenshots/
│── run.py
│── README.md
│── pyproject.toml
└── database.db (optional)


License
MIT License.
