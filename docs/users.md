# Users API

## `GET /users/{user_id}`

**Summary**: Retrieve a user by their unique identifier.  
**Method**: GET  
**Path Parameter**:
- `user_id` (UUID) – Unique identifier of the user.

### Responses:
- **200 OK**
    - **Content**: `UserResponse`
    - **Description**: User found and returned.
- **422 Unprocessable Entity**
    - **Description**: Validation error (e.g., invalid UUID format).
- **404 Not Found**
    - **Description**: User with given `user_id` not found.

---

## `POST /users/`

**Summary**: Create a new user.  
**Method**: POST  
**Request Body**:
- `UserCreate` — Includes fields:
    - `login` (str)
    - `password` (str)
    - `background` (str)
    - `education` (str)
    - `goals` (str)
    - `goal_vacancy` (str)
    - `skills` (List[UserSkill])

### Responses:
- **201 Created**
    - **Content**: `UserResponse`
    - **Description**: User successfully created.
    - **Headers**:
        - `Location: /users/{user_id}`
- **422 Unprocessable Entity**
    - **Description**: Validation error (e.g., required fields missing or invalid).

---

## `PUT /users/`

**Summary**: Update an existing user.  
**Method**: PUT  
**Request Body**:
- `UserUpdate` — Requires `user_id`, and allows optional updates to other fields.

### Responses:
- **200 OK**
    - **Content**: `UserResponse`
    - **Description**: User successfully updated.
- **422 Unprocessable Entity**
    - **Description**: Validation error in request body.
- **404 Not Found**
    - **Description**: User with given `user_id` not found.

---

## `DELETE /users/{user_id}`

**Summary**: Delete a user by their unique identifier.  
**Method**: DELETE  
**Path Parameter**:
- `user_id` (UUID) – Unique identifier of the user to be deleted.

### Responses:
- **204 No Content**
    - **Description**: User successfully deleted.
- **422 Unprocessable Entity**
    - **Description**: Validation error (e.g., invalid UUID).
- **404 Not Found**
    - **Description**: User not found.
