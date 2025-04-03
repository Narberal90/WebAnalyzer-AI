# AI Chatbot Web Application

## Description

This project is a web application similar to ChatGPT, featuring user authentication, website analysis, and message history storage.

The project consists of:

- **Backend**: FastAPI, PostgreSQL, SQLAlchemy.
- **Frontend**: React (Vite).
- **Docker**: Containers for backend, frontend, and PostgreSQL database.

## Technologies

- **Backend**: FastAPI, SQLAlchemy, OpenAI API.
- **Frontend**: React, Vite, Axios.
- **Database**: PostgreSQL.
- **Containerization**: Docker, Docker Compose.
- **Authentication**: JWT.

## Installation & Setup

### 1. Clone the Repository

```sh
git clone https://github.com/Narberal90/rai-test.git
cd rai-test
```

### 2. Environment Variables

Create `.env` files for the backend and database based on `.env.example`.

#### `.env` for Backend:

```ini
POSTGRES_HOST=db
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=dbname
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Run with Docker

```sh
docker-compose up --build
```

This will start the following services:

- **Frontend**: [http://localhost:5000](http://localhost:5000)
- **Backend**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Database**: PostgreSQL

## Project Structure

```
.
├── backend/          # Backend using FastAPI
│   ├── app/
│   │   ├── auth/     # Authentication (JWT)
│   │   ├── message/  # CRUD for messages
│   │   ├── user/     # User management
│   │   ├── config.py # Environment configuration
│   │   ├── database.py # Database setup
│   │   ├── open_ai.py # OpenAI API integration
├── frontend/         # Frontend using React + Vite
│   ├── src/
│   │   ├── components/ # UI Components
│   │   ├── pages/     # Application pages
│   │   ├── styles/    # CSS Styles
│   ├── vite.config.js # Vite configuration
│   ├── package.json  # Dependencies
├── docker-compose.yml # Docker configuration
├── README.md
```

## Author

Yaroslav Havryliuk
