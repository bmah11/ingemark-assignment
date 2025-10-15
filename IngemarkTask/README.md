# Message Persistence Service

### Overview

The service is built with Python using the FastAPI framework and connects to a PostgreSQL database.

### Features

- Endpoints for creating, retrieving, and updating messages (CRU).
- All endpoints are secured and require a valid API key.
- Uses Pydantic models to ensure data integrity.
- Containerized with Docker and Docker Compose.
- Interactive API documentation by Swagger UI and ReDoc.
- Tests for all endpoints using *pytest*.

### Technology Stack

- Backend: Python
- Framework: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Data Validation: Pydantic
- Testing: pytest & httpx
- Containerization**:** Docker & Docker Compose
- ASGI Server**:** Uvicorn

### Prerequisites

Docker and Docker Compose.

### Running the application

1. Clone the repository.
2. Navigate to the project directory in terminal.
3. Run the following command:

   ```bash
   docker compose up --build
   ```

This command will:

* build the Docker images
* start the database
* run the web service

### Running the tests

Tesr can be run in another terminal when the application is running.

Run the following command:

```bash
docker compose exec web pytest
```

You should see an output indicating that all 3 tests passed.

### Accessing the interactive documentation

Interact with the API through:

- Swagger UI: http://localhost:8000/docs
- ReDoc**:** http://localhost:8000/redoc

### Authentication

All endpoints are protected.

1. On the /docs page, click the *Authorize* button on the top right.
2. In the *APIKeyHeader* dialog, enter *secret-key* as the value.
3. Click *Authorize.*

To use the interactive docs you must first authorize the session.

### Endpoints

The following endpoints are available:

- POST /messages/

  - Creates a new message and saves it to the database.
  - Request body: JSON object with *chat_id, content, sent_at, rating, role*.
- GET /messages/

  - Retrieves a list of all messages stored in the database.
- PUT /messages/{message_id}

  - Updates an existing message by its *message_id*.
  - Request body: JSON object with the fields to be updated.

### Example usage

Create a new message using:

```bash
curl -X 'POST' \
  'http://localhost:8000/messages/' \
  -H 'accept: application/json' \
  -H 'X-API-Key: secret-key' \
  -H 'Content-Type: application/json' \
  -d '{
  "chat_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
  "content": "Hello, World!",
  "sent_at": "2025-10-09T12:00:00Z",
  "rating": True,
  "role": "user"
}'
```
