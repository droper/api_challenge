# API Rate Limiter with Flask

This is a simple Flask application that implements a rate limiter at the API gateway level using the Fixed Window Counter algorithm, leveraging Redis for state management. The rate limiter uses JWT tokens to identify users and applies rate limits accordingly.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/api_challenge.git
    cd api_challenge
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Set up your environment variables by creating a `.env` file in the root directory and defining the following variables:

    ```bash
    REQUESTS_PER_MINUTE=100
    ```

    Adjust `REQUESTS_PER_MINUTE` as needed to define the rate limit.

2. Run the Flask application:

    ```bash
    python app.py
    ```

3. Make API requests to `http://localhost:5000/api` with a valid JWT token in the `Authorization` header.

## API Endpoints

### `POST /api`

- **Description:** Endpoint for API requests.
- **Request Headers:**
  - `Authorization`: JWT token
- **Response:**
  - `200 OK`: Request accepted.
  - `401 Unauthorized`: Authorization token required.
  - `429 Too Many Requests`: Rate limit exceeded. Retry after specified time.

## Dependencies

- Flask: Web framework for building the API.
- Redis: In-memory data structure store for rate limiting.
- python-dotenv: Library for managing environment variables.