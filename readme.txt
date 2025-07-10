csv_uploader_api
A FastAPI backend for uploading, validating, storing, querying, and managing CSV data with SQLite, API logging, token-based authentication, and more.

Features
Upload CSV files via REST API

Data validation (missing values, type checks)

Store validated data in SQLite

Query, filter, search, and delete records via API

Log all API requests to a file

Token-based authentication

View API logs via endpoint

Automatic interactive API documentation (Swagger UI)

Setup Instructions
1. Clone or Create the Project
If you have a starter script, run it. Otherwise, create the folder structure and files as described in your project documentation.

2. Prepare Your Environment
a. Create a Python virtual environment (recommended):

bash
python -m venv .venv
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
b. Install the requirements:

Make sure you have a requirements.txt file with the following:

text
fastapi
uvicorn
pydantic
python-dotenv
sqlalchemy
pandas
python-multipart
passlib[bcrypt]
Then install all dependencies:

bash
pip install -r requirements.txt
3. Configure Environment Variables
Create a .env file in your project root with:

text
DATABASE_URL=sqlite:///./data.db
API_TOKEN=supersecrettoken
LOG_FILE=app.log
You can change API_TOKEN to any secret token you prefer.

4. Initialize the Database
Before running the API, create the SQLite database and tables.

Option 1: Python Shell

bash
python
Then, in the Python shell:

python
from app.db.database import Base, engine
from app.models.data import Data
Base.metadata.create_all(bind=engine)
exit()
Option 2: Initialization Script

Create a file init_db.py with:

python
from app.db.database import Base, engine
from app.models.data import Data
Base.metadata.create_all(bind=engine)
Run it:

bash
python init_db.py
5. Start the API Server
From your project root (csv_uploader_api):

bash
uvicorn app.main:app --reload
The API will be available at: http://127.0.0.1:8000

Interactive docs: http://127.0.0.1:8000/docs

Usage
Authentication
All endpoints require a Bearer token in the Authorization header.

Example:

text
Authorization: Bearer supersecrettoken
Replace supersecrettoken with your own token if you changed it in .env.

Upload CSV
Endpoint: POST /upload

Header: Authorization: Bearer <API_TOKEN>

Form field: file (CSV file)

Sample CSV format:

text
name,age
Priya,22
Rahul,34
Meena,29
Sanjay,41
Tanvi,27
Example using curl:

bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -H "Authorization: Bearer supersecrettoken" \
  -F "file=@sample_data.csv"
Query and Manage Data
Endpoint	Method	Description
/data	GET	Get all data (with skip/limit pagination)
/data/search	GET	Filter/search by name substring and/or age range
/data/{data_id}	DELETE	Delete a record by its ID
/logs	GET	View API logs (plain text)
Examples:

Get all data:
GET /data?skip=0&limit=100

Search/filter:
GET /data/search?name=Rahul&min_age=20&max_age=40

Delete a record:
DELETE /data/5

View logs:
GET /logs

All requests must include the Authorization header.

API Documentation
Visit http://127.0.0.1:8000/docs for interactive Swagger UI documentation and testing.

Troubleshooting
Dependency errors: Ensure your virtual environment is activated and pip install -r requirements.txt completes without errors.

Database errors: Make sure you have initialized the database and tables before starting the API.

Authentication errors: Double-check your Authorization header format and token value.

Project Structure (Typical)
text
csv_uploader_api/
├── app/
│   ├── api/
│   │   └── endpoints.py
│   ├── core/
│   │   ├── auth.py
│   │   └── config.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   └── data.py
│   ├── schemas/
│   │   └── data.py
│   ├── utils/
│   │   └── logger.py
│   └── main.py
├── .env
├── requirements.txt
├── README.md
└── sample_data.csv
Quick Start Checklist
Clone/setup project files and folders.

Create and activate a virtual environment.

Install requirements.

Configure .env.

Initialize the database.

Start the API server.

Use Swagger UI or curl to test endpoints.

You’re all set!
For any issues, check your logs (app.log) or reach out for help.