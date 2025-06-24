# Roadmap API

## `GET /roadmap/{roadmap_id}`

**Summary**: Get Roadmap
**Method**: GET
**Path Parameter**:

* `roadmap_id` (UUID) — Unique identifier of the roadmap to retrieve.

**Example Request**:

```bash
curl -X GET "https://api.example.com/roadmap/123e4567-e89b-12d3-a456-426614174001"
```

**Responses**:

* `200 OK`: `RoadmapInfo`

  * **Example Response**:

    ```json
    {
      "roadmap_id": "123e4567-e89b-12d3-a456-426614174001",
      "nodes": [...],
      "links": [...]
    }
    ```
* `404 Not Found`:

  * **Example Response**:

    ```json
    {
      "detail": "Roadmap not found"
    }
    ```
* `422 Unprocessable Entity`: Validation Error

  * **Example Response**:

    ```json
    {
      "detail": [
        {
          "loc": ["path", "roadmap_id"],
          "msg": "value is not a valid uuid",
          "type": "type_error.uuid"
        }
      ]
    }
    ```
* `500 Internal Server Error`:

  * **Example Response**:

    ```json
    {
      "detail": "Internal server error"
    }
    ```

---

## `POST /roadmap/`

**Summary**: Post Roadmap
**Method**: POST
**Body**: `RoadmapCreate` (поле `user_id`)

**Example Request Body**:

```json
{
  "user_id": "456e4567-e89b-12d3-a456-426614174999"
}
```

**Example cURL**:

```bash
curl -X POST "https://api.example.com/roadmap/" \
  -H "Content-Type: application/json" \
  -d '{
        "user_id": "456e4567-e89b-12d3-a456-426614174999"
      }'
```

**Responses**:

* `201 Created`: `RoadmapResponse`

  * **Headers**:

    ```http
    Location: /roadmap/123e4567-e89b-12d3-a456-426614174001
    ```
  * **Example Response**:

    ```json
    {
      "roadmap_id": "123e4567-e89b-12d3-a456-426614174001",
      "user_id": "456e4567-e89b-12d3-a456-426614174999"
    }
    ```
* `400 Bad Request`: Business rule violation

  * **Example Response**:

    ```json
    {
      "detail": "User already has a roadmap"
    }
    ```
* `422 Unprocessable Entity`: Validation Error

  * **Example Response**:

    ```json
    {
      "detail": [
        {
          "loc": ["body", "user_id"],
          "msg": "field required",
          "type": "value_error.missing"
        }
      ]
    }
    ```
* `500 Internal Server Error`:

  * **Example Response**:

    ```json
    {
      "detail": "Internal server error"
    }
    ```

---

## `PUT /roadmap/`

**Summary**: Put Roadmap
**Method**: PUT
**Body**: `RoadmapUpdate`

**Example Request Body**:

```json
{
  "roadmap_id": "123e4567-e89b-12d3-a456-426614174001",
  "user_id": "456e4567-e89b-12d3-a456-426614174999"
}
```

**Example cURL**:

```bash
curl -X PUT "https://api.example.com/roadmap/" \
  -H "Content-Type: application/json" \
  -d '{
        "roadmap_id": "123e4567-e89b-12d3-a456-426614174001",
        "user_id": "456e4567-e89b-12d3-a456-426614174999"
      }'
```

**Responses**:

* `200 OK`: `RoadmapResponse`

  * **Example Response**:

    ```json
    {
      "roadmap_id": "123e4567-e89b-12d3-a456-426614174001",
      "user_id": "456e4567-e89b-12d3-a456-426614174999"
    }
    ```
* `400 Bad Request`: No fields provided or invalid

  * **Example Response**:

    ```json
    {
      "detail": "No fields provided for update"
    }
    ```
* `404 Not Found`: Roadmap not found

  * **Example Response**:

    ```json
    {
      "detail": "Roadmap not found"
    }
    ```
* `422 Unprocessable Entity`: Validation Error

  * **Example Response**:

    ```json
    {
      "detail": [
        {
          "loc": ["body", "roadmap_id"],
          "msg": "value is not a valid uuid",
          "type": "type_error.uuid"
        }
      ]
    }
    ```
* `500 Internal Server Error`:

  * **Example Response**:

    ```json
    {
      "detail": "Internal server error"
    }
    ```

---

## `DELETE /roadmap/{roadmap_id}`

**Summary**: Delete Roadmap
**Method**: DELETE
**Path Parameter**:

* `roadmap_id` (UUID) — Unique identifier of the roadmap to delete.

**Example Request**:

```bash
curl -X DELETE "https://api.example.com/roadmap/123e4567-e89b-12d3-a456-426614174001"
```

**Responses**:

* `204 No Content`: Success (no body)
* `404 Not Found`: Roadmap not found

  * **Example Response**:

    ```json
    {
      "detail": "Roadmap not found"
    }
    ```
* `422 Unprocessable Entity`: Validation Error

  * **Example Response**:

    ```json
    {
      "detail": [
        {
          "loc": ["path", "roadmap_id"],
          "msg": "value is not a valid uuid",
          "type": "type_error.uuid"
        }
      ]
    }
    ```
* `500 Internal Server Error`:

  * **Example Response**:

    ```json
    {
      "detail": "Internal server error"
    }
    ```
