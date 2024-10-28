
## Installation

1. Clone the repository.
2. Install dependencies:
    ```bash
    poetry install
    ```
3. Create a `.env` file from `.env.example`:
 
4. Apply database migrations with Alembic:
    ```bash
    poetry run alembic upgrade head
    ```
5. Start the server:
    ```bash
    poetry run uvicorn src.main:app --reload
    ```

## Usage

TThe project provides APIs for managing posts and comments with automated moderation. You can interact with the API endpoints through Swagger at http://localhost:8000/docs

### Endpoints
- `POST /api/post`: Create a new post.
- `GET /api/post/{post_id}`: Get a post by ID.
- `PATCH /api/post/{post_id}`: Update a post by ID.
- `DELETE /api/post/{post_id}`: Delete a post by ID.
- `POST /api/post/{post_id}/comment`: Add a comment to a post.
- `GET /api/comments-daily-breakdown`: Get a daily breakdown of comment activity.
- `POST /auth/register:`: Create a new user 
- `POST /auth/token:`: Login a user

### Testing

To run all tests:
 ```bash
    poetry run pytest
   ```

## Notes

- Ensure the `.env` file is correctly configured before running the application.
- The automated moderation API requires valid credentials for Google's Natural Language API, configured through `GOOGLE_API_KEY`.