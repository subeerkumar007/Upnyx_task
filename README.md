# Django Chat API

A simple RESTful chat API built with Django and Django REST Framework. It supports user registration, login, token-based authentication, chat messaging, and token balance management.

## Features

- **User Registration**: Create a new user account.
- **Login**: Authenticate and receive an API token.
- **Chat**: Send messages and receive AI responses (dummy response for now).
- **Token System**: Each user starts with 4000 tokens; each chat costs 100 tokens.
- **Balance**: Check remaining tokens.
- **Admin Panel**: Manage users, chats, and tokens.

## Project Structure

- `chatapi/`  
  - `chatapi/`  
    - Django project settings, URLs, WSGI/ASGI configs  
  - `core/`  
    - Models: `User`, `Chat`, `AuthToken`  
    - Serializers: Registration, Login, Chat request  
    - Views: API endpoints for register, login, chat, balance  
    - URLs: API routing  
    - Admin: Django admin customizations  
    - Migrations: Database schema  
  - `db.sqlite3`: SQLite database  
  - `manage.py`: Django management script  
  - `requirements.txt`: Dependencies

## API Endpoints

| Endpoint      | Method | Description                |
|---------------|--------|---------------------------|
| `/register/`  | POST   | Register a new user       |
| `/login/`     | POST   | Login and get token       |
| `/chat/`      | POST   | Send a chat message       |
| `/balance/`   | GET    | Get token balance         |

## Authentication

- After login, use the returned token in the `Authorization` header:  
  `Authorization: Token <your_token>`
- Alternatively, include `token` in the request body for chat.

## Setup

1. **Install dependencies**  
   ```
   pip install -r requirements.txt
   ```

2. **Apply migrations**  
   ```
   python manage.py migrate
   ```

3. **Run server**  
   ```
   python manage.py runserver
   ```

4. **Access admin panel**  
   ```
   python manage.py createsuperuser
   ```
   Visit `/admin/` in your browser.

## Notes

- The chat response is currently a dummy string.
- Token deduction is atomic; users must have at least 100 tokens to chat.
- All endpoints are open (`AllowAny` permission) for demo purposes.

## License

MIT

---

**Main files:**  
- [core/models.py](core/models.py)  
- [core/views.py](core/views.py)  
- [core/serializers.py](core/serializers.py)
