# Roadmap API

## `GET /roadmap/{roadmap_id}`

**Summary**: Get Roadmap  
**Method**: GET  
**Path Parameter**:
- `roadmap_id` (UUID) — Unique identifier of the roadmap to retrieve.  
  **Responses**:
- `200 OK`: `RoadmapInfo` (включает поля `roadmap_id`, `nodes`, `links`)
- `404 Not Found`: если не найдено (`{"detail": "Roadmap not found"}`)
- `422 Unprocessable Entity`: Validation Error
- `500 Internal Server Error`: Internal server error

## `POST /roadmap/`

**Summary**: Post Roadmap  
**Method**: POST  
**Body**: `RoadmapCreate` (поле `user_id`)  
**Responses**:
- `201 Created`: `RoadmapResponse`
    - **Headers**: `Location: /roadmap/{roadmap_id}`
- `400 Bad Request`: Business rule violation (`{"detail": "..."}`)
- `422 Unprocessable Entity`: Validation Error
- `500 Internal Server Error`: Internal server error

## `PUT /roadmap/`

**Summary**: Put Roadmap  
**Method**: PUT  
**Body**: `RoadmapUpdate` (поля: `roadmap_id` обязательно, `user_id` опционально и т.д.)  
**Responses**:
- `200 OK`: `RoadmapResponse`
- `400 Bad Request`: No fields provided or business rule violation (`{"detail": "No fields provided for update"}`)
- `404 Not Found`: Roadmap not found (`{"detail": "Roadmap not found"}`)
- `422 Unprocessable Entity`: Validation Error
- `500 Internal Server Error`: Internal server error

## `DELETE /roadmap/{roadmap_id}`

**Summary**: Delete Roadmap  
**Method**: DELETE  
**Path Parameter**:
- `roadmap_id` (UUID) — Unique identifier of the roadmap to delete.  
  **Responses**:
- `204 No Content`: Success (No Content)
- `404 Not Found`: Roadmap not found (`{"detail": "Roadmap not found"}`)
- `422 Unprocessable Entity`: Validation Error
- `500 Internal Server Error`: Internal server error
