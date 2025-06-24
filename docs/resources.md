# Resource API

## `GET /resource/{res_id}`

**Summary**: Get Resource
**Path Parameter**:

* `res_id` (UUID)

**Example Request**:

```bash
curl -X GET "https://api.example.com/resource/123e4567-e89b-12d3-a456-426614174001"
```

**Responses**:

* `200 OK`: `ResourceResponse`

  * **Example Response**:

    ```json
    {
      "res_id": "123e4567-e89b-12d3-a456-426614174001",
      "title": "Документация по API",
      "url": "https://example.com/docs",
      "node_id": "223e4567-e89b-12d3-a456-426614174002"
    }
    ```
* `404 Not Found`: Resource not found

  * **Example Response**:

    ```json
    {
      "detail": "Resource not found"
    }
    ```
* `422 Unprocessable Entity`: Validation Error

  * **Example Response**:

    ```json
    {
      "detail": [
        {
          "loc": ["path", "res_id"],
          "msg": "value is not a valid uuid",
          "type": "type_error.uuid"
        }
      ]
    }
    ```

---

## `POST /resource/`

**Summary**: Post Resource
**Body**: `ResourceCreate`

**Example Request**:

```json
{
  "title": "Гайд по FastAPI",
  "url": "https://fastapi.tiangolo.com/",
  "node_id": "223e4567-e89b-12d3-a456-426614174002"
}
```

**Example cURL**:

```bash
curl -X POST "https://api.example.com/resource/" \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Гайд по FastAPI",
        "url": "https://fastapi.tiangolo.com/",
        "node_id": "223e4567-e89b-12d3-a456-426614174002"
      }'
```

**Responses**:

* `200 OK`: `ResourceResponse`

  * **Example Response**:

    ```json
    {
      "res_id": "123e4567-e89b-12d3-a456-426614174010",
      "title": "Гайд по FastAPI",
      "url": "https://fastapi.tiangolo.com/",
      "node_id": "223e4567-e89b-12d3-a456-426614174002"
    }
    ```
* `400 Bad Request`: Duplicate or business rule violation

  * **Example Response**:

    ```json
    {
      "detail": "Resource with this URL already exists for the given node"
    }
    ```
* `422 Unprocessable Entity`: Validation Error

  * **Example Response**:

    ```json
    {
      "detail": [
        {
          "loc": ["body", "title"],
          "msg": "field required",
          "type": "value_error.missing"
        }
      ]
    }
    ```

---

## `PUT /resource/`

**Summary**: Put Resource
**Body**: `ResourceUpdate`

**Example Request**:

```json
{
  "res_id": "123e4567-e89b-12d3-a456-426614174010",
  "title": "FastAPI Руководство",
  "url": "https://fastapi.tiangolo.com/ru/"
}
```

**Example cURL**:

```bash
curl -X PUT "https://api.example.com/resource/" \
  -H "Content-Type: application/json" \
  -d '{
        "res_id": "123e4567-e89b-12d3-a456-426614174010",
        "title": "FastAPI Руководство",
        "url": "https://fastapi.tiangolo.com/ru/"
      }'
```

**Responses**:

* `200 OK`: `ResourceResponse`

  * **Example Response**:

    ```json
    {
      "res_id": "123e4567-e89b-12d3-a456-426614174010",
      "title": "FastAPI Руководство",
      "url": "https://fastapi.tiangolo.com/ru/",
      "node_id": "223e4567-e89b-12d3-a456-426614174002"
    }
    ```
* `400 Bad Request`: No fields provided

  * **Example Response**:

    ```json
    {
      "detail": "At least one updatable field must be provided"
    }
    ```
* `404 Not Found`: Resource not found

  * **Example Response**:

    ```json
    {
      "detail": "Resource not found"
    }
    ```
* `422 Unprocessable Entity`: Validation Error

  * **Example Response**:

    ```json
    {
      "detail": [
        {
          "loc": ["body", "res_id"],
          "msg": "value is not a valid uuid",
          "type": "type_error.uuid"
        }
      ]
    }
    ```

---

## `DELETE /resource/{res_id}`

**Summary**: Delete Resource
**Path Parameter**:

* `res_id` (UUID)

**Example Request**:

```bash
curl -X DELETE "https://api.example.com/resource/123e4567-e89b-12d3-a456-426614174010"
```

**Responses**:

* `204 No Content`: Success (No response body)
* `404 Not Found`: Resource not found

  * **Example Response**:

    ```json
    {
      "detail": "Resource not found"
    }
    ```
* `422 Unprocessable Entity`: Validation Error

  * **Example Response**:

    ```json
    {
      "detail": [
        {
          "loc": ["path", "res_id"],
          "msg": "value is not a valid uuid",
          "type": "type_error.uuid"
        }
      ]
    }
    ```
