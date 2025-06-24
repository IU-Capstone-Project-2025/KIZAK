# Resource API

## `GET /resource/{res_id}`

**Summary**: Get Resource  
**Path Parameter**:
- `res_id` (UUID)  
  **Responses**:
- `200`: `ResourceResponse`
- `404`: Resource not found
- `422`: Validation Error

## `POST /resource/`

**Summary**: Post Resource  
**Body**: `ResourceCreate`  
**Responses**:
- `200`: `ResourceResponse`
- `400`: Bad Request (e.g., business rule violation such as duplicate)
- `422`: Validation Error

## `PUT /resource/`

**Summary**: Put Resource  
**Body**: `ResourceUpdate`  
**Responses**:
- `200`: `ResourceResponse`
- `400`: Bad Request (e.g., no fields provided for update)
- `404`: Resource not found
- `422`: Validation Error

## `DELETE /resource/{res_id}`

**Summary**: Delete Resource  
**Path Parameter**:
- `res_id` (UUID)  
  **Responses**:
- `204`: Success (No Content)
- `404`: Resource not found
- `422`: Validation Error
