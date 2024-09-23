# Auctions

## Description
This is a Django-based web application for managing online auctions. Users can create listings, place bids, and leave comments on items for sale. The platform provides real-time bidding.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yahoo-24/auction-platform.git
2. Navigate to the project directory:
   ```bash
   cd auction-platform
3. Create a virtual environment and activate it:
   ```bash
   python3 -m venv env
   source env/bin/activate
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
5. Run the migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver

### Usage Instructions
1. Open your browser and go to http://localhost:8000.
2. Register an account, create an auction listing, and place bids.

## Features
- User authentication and registration.
- Real-time bidding.
- Create and manage listings.
- Commenting system.

## Technologies Used
- Django (Backend)
- HTML/CSS (Frontend)
- SQLite (Database)
