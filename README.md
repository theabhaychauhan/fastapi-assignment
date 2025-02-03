# FastAPI Assignment

## Description

This project is a web application that integrates with the Binance API to display cryptocurrency prices and allow user authentication and profile management. It consists of a FastAPI backend and a React frontend.

## Prerequisites

- Python 3.7 or higher
- Node.js 14 or higher
- PostgreSQL (or another database supported by SQLAlchemy)

## Setup Instructions

### Backend Setup

1. **Clone the Repository**

git clone https://github.com/theabhaychauhan/fastapi-assignment.git
cd fastapi-assignment/backend


2. **Create Environment Variables**

Copy the example environment file and rename it to .env and change your secrets:


Update the `.env` file with your actual configuration values, such as database connection details.

3. **Update Alembic Configuration**

Open `alembic.ini` and change the `sqlalchemy.url` to match your database connection string:


4. **Install Dependencies**

Ensure you have the required Python packages installed:

pip install -r requirements.txt


5. **Run Database Migrations**

Apply migrations to set up your database schema:

alembic upgrade head


6. **Start the FastAPI Server**

Start the Uvicorn server:

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


### Frontend Setup

1. **Navigate to the Frontend Directory**

cd ../frontend

2. **Install Frontend Dependencies**

Install the required Node.js packages:

npm install


3. **Start the React Development Server**

Start the Node server:

npm start


4. **Access the Application**

Open your web browser and go to:

http://localhost:5173
