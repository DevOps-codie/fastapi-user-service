# FastAPI User Service

A Dockerized REST API for managing users with FastAPI and PostgreSQL. This service supports creating, reading, updating, and deleting user records using either email or SMS for identification.

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/fastapi-user-service.git
cd fastapi-user-service
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root with the following content:

```plaintext
DATABASE_URL=postgresql://user:password@db:5432/mydatabase
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=mydatabase
```

### 3. Initialize the Database

The `init.sql` file sets up the `users` table automatically. To ensure the database initializes correctly, bring down any existing volumes first:

```bash
docker compose down --volumes
```

### 4. Build and Start Services

Run the following command to start the application in detached mode:

```bash
docker compose up -d
```

This will start both the `db` (PostgreSQL) and `web` (FastAPI) services. The API will be accessible at `http://localhost:8088`.

### 5. Run Tests

To run tests after the services are up:

```bash
docker compose exec web pytest test-main.py
```

This command will execute the tests in the `test-main.py` file. Ensure that the database is correctly initialized before running tests to avoid table-related errors.

### API Endpoints

- **Get All Users**: `GET /users`
- **Get User by ID**: `GET /users/{userid}`
- **Create User**: `POST /users` (requires either `email` or `sms`)
- **Update User**: `PUT /users/{userid}`
- **Delete User**: `DELETE /users/{userid}`

### Example Requests

Create a user:
```bash
curl -X POST "http://localhost:8088/users" -H "Content-Type: application/json" -d '{"email": "user@example.com"}'
```

Get all users:
```bash
curl http://localhost:8088/users
```

### Stop Services

To stop and remove containers:

```bash
docker compose down
```

---

