# Users API

## `GET /users/{user_id}`

**Summary**: Retrieve a user by their unique identifier.
**Method**: GET
**Path Parameter**:

* `user_id` (UUID) – Unique identifier of the user.

**Example Request**:

```bash
curl -X GET "https://api.example.com/users/123e4567-e89b-12d3-a456-426614174001"
```

### Responses:

* **200 OK**

  * **Content**: `UserResponse`
  * **Example Response**:

    ```json
    {
      "user_id": "123e4567-e89b-12d3-a456-426614174001",
      "login": "johndoe",
      "background": "backend development",
      "education": "BS Computer Science",
      "goals": "become senior developer",
      "goal_vacancy": "Python Developer",
      "skills": [
        {"name": "Python", "level": "advanced"},
        {"name": "Docker", "level": "intermediate"}
      ]
    }
    ```
* **422 Unprocessable Entity**

  * **Example Response**:

    ```json
    {
      "detail": [
        {
          "loc": ["path", "user_id"],
          "msg": "value is not a valid uuid",
          "type": "type_error.uuid"
        }
      ]
    }
    ```
* **404 Not Found**

  * **Example Response**:

    ```json
    {
      "detail": "User not found"
    }
    ```

---

## `POST /users/`

**Summary**: Create a new user.
**Method**: POST
**Request Body**:

* `UserCreate`

**Example Request Body**:

```json
{
  "login": "johndoe",
  "password": "securePass123",
  "background": "backend development",
  "education": "BS Computer Science",
  "goals": "become senior developer",
  "goal_vacancy": "Python Developer",
  "skills": [
    {"name": "Python", "level": "advanced"},
    {"name": "Git", "level": "intermediate"}
  ]
}
```

**Example cURL**:

```bash
curl -X POST "https://api.example.com/users/" \
  -H "Content-Type: application/json" \
  -d '{
        "login": "johndoe",
        "password": "securePass123",
        "background": "backend development",
        "education": "BS Computer Science",
        "goals": "become senior developer",
        "goal_vacancy": "Python Developer",
        "skills": [
          {"name": "Python", "level": "advanced"},
          {"name": "Git", "level": "intermediate"}
        ]
      }'
```

### Responses:

* **201 Created**

  * **Headers**:

    ```http
    Location: /users/123e4567-e89b-12d3-a456-426614174001
    ```
  * **Example Response**:

    ```json
    {
      "user_id": "123e4567-e89b-12d3-a456-426614174001",
      "login": "johndoe",
      "background": "backend development",
      "education": "BS Computer Science",
      "goals": "become senior developer",
      "goal_vacancy": "Python Developer",
      "skills": [
        {"name": "Python", "level": "advanced"},
        {"name": "Git", "level": "intermediate"}
      ]
    }
    ```
* **422 Unprocessable Entity**

  * **Example Response**:

    ```json
    {
      "detail": [
        {
          "loc": ["body", "login"],
          "msg": "field required",
          "type": "value_error.missing"
        }
      ]
    }
    ```

---

## `PUT /users/`

**Summary**: Update an existing user.
**Method**: PUT
**Request Body**:

* `UserUpdate`

**Example Request Body**:

```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174001",
  "background": "fullstack development",
  "skills": [
    {"name": "React", "level": "beginner"},
    {"name": "Python", "level": "expert"}
  ]
}
```

**Example cURL**:

```bash
curl -X PUT "https://api.example.com/users/" \
  -H "Content-Type: application/json" \
  -d '{
        "user_id": "123e4567-e89b-12d3-a456-426614174001",
        "background": "fullstack development",
        "skills": [
          {"name": "React", "level": "beginner"},
          {"name": "Python", "level": "expert"}
        ]
      }'
```

### Responses:

* **200 OK**

  * **Example Response**:

    ```json
    {
      "user_id": "123e4567-e89b-12d3-a456-426614174001",
      "login": "johndoe",
      "background": "fullstack development",
      "education": "BS Computer Science",
      "goals": "become senior developer",
      "goal_vacancy": "Python Developer",
      "skills": [
        {"name": "React", "level": "beginner"},
        {"name": "Python", "level": "expert"}
      ]
    }
    ```
* **422 Unprocessable Entity**

  * **Example Response**:

    ```json
    {
      "detail": [
        {
          "loc": ["body", "user_id"],
          "msg": "value is not a valid uuid",
          "type": "type_error.uuid"
        }
      ]
    }
    ```
* **404 Not Found**

  * **Example Response**:

    ```json
    {
      "detail": "User not found"
    }
    ```

---

## `DELETE /users/{user_id}`

**Summary**: Delete a user by their unique identifier.
**Method**: DELETE
**Path Parameter**:

* `user_id` (UUID) – Unique identifier of the user to be deleted.

**Example Request**:

```bash
curl -X DELETE "https://api.example.com/users/123e4567-e89b-12d3-a456-426614174001"
```

### Responses:

* **204 No Content**
* **422 Unprocessable Entity**

  * **Example Response**:

    ```json
    {
      "detail": [
        {
          "loc": ["path", "user_id"],
          "msg": "value is not a valid uuid",
          "type": "type_error.uuid"
        }
      ]
    }
    ```
* **404 Not Found**

  * **Example Response**:

    ```json
    {
      "detail": "User not found"
    }
    ```
