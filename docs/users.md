# Users API

## `GET /users/{user_id}`

**Summary**: Get User  
**Path Parameter**:
- `user_id` (UUID) – User identifier  
**Responses**:
- `200`: `UserResponse`
- `422`: Validation Error

## `POST /users/`

**Summary**: Post User  
**Body**: `UserCreate`  
**Responses**:
- `201`: `UserResponse`
- `422`: Validation Error

## `PUT /users/`

**Summary**: Put User  
**Body**: `UserUpdate`  
**Responses**:
- `200`: `UserResponse`
- `422`: Validation Error

## `DELETE /users/{user_id}`

**Summary**: Delete User  
**Path Parameter**:
- `user_id` (UUID)  
**Responses**:
- `204`: Success
- `422`: Validation Error
