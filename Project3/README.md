# Wiki

## Description
This is a Django-based web application for Wikipedia-like pages. Users can create wiki pages, open wiki pages, modify wiki pages, and search for existing wiki pages.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yahoo-24/Free-Time-Projects.git
2. Navigate to the project directory:
   ```bash
   cd Project3
   cd wiki
3. Create a virtual environment and activate it:
   ```bash
   python3 -m venv env
   source env/bin/activate
4. Install dependencies:
   ```bash
   pip install -r requirement.txt
5. Run the migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver

### Usage Instructions
1. Open your browser and go to http://localhost:8000.
2. Modify, create new pages or simply look through some of the existing pages.

## Features
- Adding new pages.
- Modifying existing pages.
- Searching for specific pages.

## Technologies Used
- Django (Backend)
- HTML/CSS (Frontend)
- SQLite (Database)
