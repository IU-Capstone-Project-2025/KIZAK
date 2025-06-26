# Node API

## `GET /node/{node_id}`

**Summary**: Get Node
**Method**: GET
**Path Parameter**:

* `node_id` (UUID)

**Responses**:

* `200 OK`: `NodeResponse`

    * **Example Request**:

      ```bash
      curl -X GET "https://api.example.com/node/123e4567-e89b-12d3-a456-426614174001"
      ```
    * **Example Response**:

      ```json
      {
        "node_id": "123e4567-e89b-12d3-a456-426614174001",
        "roadmap_id": "123e4567-e89b-12d3-a456-426614174005",
        "title": "Пример узла",
        "description": "Описание данного узла"
      }
      ```
* `404 Not Found`: Node not found

    * **Example Response**:

      ```json
      {
        "detail": "Node not found"
      }
      ```
* `422 Unprocessable Entity`: Validation Error

    * **Example Request with invalid UUID**:

      ```bash
      curl -X GET "https://api.example.com/node/invalid-uuid"
      ```
    * **Example Response**:

      ```json
      {
        "detail": [
          {
            "loc": ["path", "node_id"],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
          }
        ]
      }
      ```

---

## `POST /node/`

**Summary**: Create Node
**Method**: POST
**Body**: `NodeCreate`

**Example Request Body**:

```json
{
  "roadmap_id": "123e4567-e89b-12d3-a456-426614174005",
  "title": "Новый узел",
  "description": "Описание нового узла"
}
```

**Example cURL**:

```bash
curl -X POST "https://api.example.com/node/" \
  -H "Content-Type: application/json" \
  -d '{
        "roadmap_id": "123e4567-e89b-12d3-a456-426614174005",
        "title": "Новый узел",
        "description": "Описание нового узла"
      }'
```

**Responses**:

* `201 Created`: `NodeResponse`

    * **Example Response**:

      ```json
      {
        "node_id": "223e4567-e89b-12d3-a456-426614174010",
        "roadmap_id": "123e4567-e89b-12d3-a456-426614174005",
        "title": "Новый узел",
        "description": "Описание нового узла"
      }
      ```
* `400 Bad Request`: Business rule violation

    * **Example Response**:

      ```json
      {
        "detail": "Business rule violation: Node with this title already exists in the roadmap"
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

## `PUT /node/`

**Summary**: Update Node
**Method**: PUT
**Body**: `NodeUpdate`

**Example Request Body**:

```json
{
  "node_id": "223e4567-e89b-12d3-a456-426614174010",
  "title": "Обновлённое название узла",
  "description": "Обновлённое описание"
}
```

**Example cURL**:

```bash
curl -X PUT "https://api.example.com/node/" \
  -H "Content-Type: application/json" \
  -d '{
        "node_id": "223e4567-e89b-12d3-a456-426614174010",
        "title": "Обновлённое название узла",
        "description": "Обновлённое описание"
      }'
```

**Responses**:

* `200 OK`: `NodeResponse`

    * **Example Response**:

      ```json
      {
        "node_id": "223e4567-e89b-12d3-a456-426614174010",
        "roadmap_id": "123e4567-e89b-12d3-a456-426614174005",
        "title": "Обновлённое название узла",
        "description": "Обновлённое описание"
      }
      ```
* `400 Bad Request`: Business rule violation

    * **Example Response**:

      ```json
      {
        "detail": "Business rule violation: Title cannot be empty"
      }
      ```
* `404 Not Found`: Node not found

    * **Example Response**:

      ```json
      {
        "detail": "Node not found"
      }
      ```
* `422 Unprocessable Entity`: Validation Error

    * **Example Response**:

      ```json
      {
        "detail": [
          {
            "loc": ["body", "node_id"],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
          }
        ]
      }
      ```

---

## `DELETE /node/{node_id}`

**Summary**: Delete Node
**Method**: DELETE
**Path Parameter**:

* `node_id` (UUID)

**Example Request**:

```bash
curl -X DELETE "https://api.example.com/node/223e4567-e89b-12d3-a456-426614174010"
```

**Responses**:

* `204 No Content`: Success (без тела)
* `404 Not Found`: Node not found

    * **Example Response**:

      ```json
      {
        "detail": "Node not found"
      }
      ```
* `422 Unprocessable Entity`: Validation Error

    * **Example Response**:

      ```json
      {
        "detail": [
          {
            "loc": ["path", "node_id"],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
          }
        ]
      }
      ```
