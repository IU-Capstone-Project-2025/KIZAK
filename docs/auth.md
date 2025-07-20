# Auth API

## `POST /login/`

**Summary**: Authenticates a user and returns an access token.

**Method**: POST

**Tags**: User

**Request Body (Form Data)**:

* `username` (string) – The user's login.
* `password` (string) – The user's password.

**Example cURL**:

```bash
curl -X POST "https://api.example.com/login/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=johndoe&password=securePass123'
```

### Responses:

* **200 OK**

  ```json
  {
    "token": {
      "access_token": "<JWT token>",
      "token_type": "bearer"
    },
    "user_id": "123e4567-e89b-12d3-a456-426614174001"
  }
  ```

* **401 Unauthorized**

  ```json
  {
    "detail": "Incorrect username or password"
  }
  ```

---

## `POST /signup/`

**Summary**: Registers a new user and sends a verification email.

**Method**: POST

**Tags**: User

**Request Body**:

* `UserCreate`

**Example Request Body**:

```json
{
  "login": "johndoe",
  "password": "securePass123",
  "mail": "user@example.com"
}
```

**Example cURL**:

```bash
curl -X POST "https://api.example.com/signup/" \
  -H "Content-Type: application/json" \
  -d '{
        "login": "johndoe",
        "password": "securePass123",
        "mail": "user@example.com"
      }'
```

### Responses:

* **201 Created**

  ```json
  {
    "user_id": "123e4567-e89b-12d3-a456-426614174001",
    "login": "johndoe",
    "mail": "user@example.com",
    "is_verified": false
  }
  ```

---

## `GET /verify/{token}`

**Summary**: Verifies a user account via email token.

**Method**: GET

**Tags**: User

**Path Parameter**:

* `token` (string) – Verification token.

**Example Request**:

```bash
curl -X GET "https://api.example.com/verify/sometoken123"
```

### Responses:

* **200 OK**

  ```json
  {
    "message": "Account verified successfully"
  }
  ```

* **500 Internal Server Error**

  ```json
  {
    "message": "Error occurred during verification"
  }
  ```

---

## `POST /password-reset-request`

**Summary**: Sends a password reset email to the user.

**Method**: POST

**Tags**: User

**Request Body**:

* `PasswordResetRequestModel`

    * `mail` (string) – The user's email address.

**Example Request Body**:

```json
{
  "mail": "user@example.com"
}
```

**Example cURL**:

```bash
curl -X POST "https://api.example.com/password-reset-request" \
  -H "Content-Type: application/json" \
  -d '{
        "mail": "user@example.com"
      }'
```

### Responses:

* **200 OK**

  ```json
  {
    "message": "Password reset request sent to email"
  }
  ```

---

## `POST /password-reset-confirm/{token}`

**Summary**: Resets a user's password using a confirmation token.

**Method**: POST

**Tags**: User

**Path Parameter**:

* `token` (string) – Password reset token.

**Request Body**:

* `PasswordResetConfirmModel`

    * `new_password` (string) – The new password.
    * `confirm_new_password` (string) – Password confirmation.

**Example Request Body**:

```json
{
  "new_password": "newSecurePass123",
  "confirm_new_password": "newSecurePass123"
}
```

**Example cURL**:

```bash
curl -X POST "https://api.example.com/password-reset-confirm/sometoken123" \
  -H "Content-Type: application/json" \
  -d '{
        "new_password": "newSecurePass123",
        "confirm_new_password": "newSecurePass123"
      }'
```

### Responses:

* **200 OK**

  ```json
  {
    "message": "Password reset successfully"
  }
  ```

* **400 Bad Request**

  ```json
  {
    "detail": "Passwords do not match"
  }
  ```

* **500 Internal Server Error**

  ```json
  {
    "message": "Error occurred during password reset"
  }
  ```
