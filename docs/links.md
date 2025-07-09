# Link API

## `GET /link/{link_id}`

**Summary**: Get Link  
**Method**: GET  
**Path Parameter**:
- `link_id` (UUID) — Unique identifier of the link to retrieve.

**Responses**:
- `200 OK`:
    - **Description**: Link found and returned.
    - **Content**: JSON matching model `LinkResponse`.
        - **Schema** (`LinkResponse`):
          ```json
          {
            "link_id": "UUID",
            "roadmap_id": "UUID",
            "from_node": "UUID",
            "to_node": "UUID"
          }
          ```
        - **Example**:
          ```json
          {
            "link_id": "123e4567-e89b-12d3-a456-426614174003",
            "roadmap_id": "123e4567-e89b-12d3-a456-426614174005",
            "from_node": "123e4567-e89b-12d3-a456-426614174001",
            "to_node": "123e4567-e89b-12d3-a456-426614174002"
          }
          ```
- `404 Not Found`:
    - **Description**: Link with given `link_id` not found.
    - **Content**:
      ```json
      {"detail": "Link not found"}
      ```
- `422 Unprocessable Entity`:
    - **Description**: Validation error (e.g., `link_id` is not a valid UUID).
    - **Content**: FastAPI’s standard validation error details.
- `500 Internal Server Error`:
    - **Description**: Unexpected server/database error.
    - **Content**:
      ```json
      {"detail": "Internal server error"}
      ```

---

## `POST /link/`

**Summary**: Create Link  
**Method**: POST  
**Path**: `/link/`

### Request Body
Model: `LinkCreate`, fields:
- `roadmap_id` (UUID) — Unique identifier of the roadmap.
- `from_node` (UUID) — Unique identifier of the source node.
- `to_node` (UUID) — Unique identifier of the target node.

#### Example Request Body
```json
{
  "roadmap_id": "123e4567-e89b-12d3-a456-426614174005",
  "from_node": "123e4567-e89b-12d3-a456-426614174001",
  "to_node": "123e4567-e89b-12d3-a456-426614174002"
}
