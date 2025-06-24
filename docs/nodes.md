# Node API

## `GET /node/{node_id}`

**Summary**: Get Node  
**Method**: GET  
**Path Parameter**:
- `node_id` (UUID)

**Responses**:
- `200`: `NodeResponse`
- `404`: Node not found
- `422`: Validation Error

---

## `POST /node/`

**Summary**: Create Node  
**Method**: POST  
**Body**: `NodeCreate`

**Responses**:
- `201`: `NodeResponse`
- `400`: Bad Request (business rule violation)
- `422`: Validation Error

---

## `PUT /node/`

**Summary**: Update Node  
**Method**: PUT  
**Body**: `NodeUpdate`

**Responses**:
- `200`: `NodeResponse`
- `400`: Bad Request (e.g., no fields provided or business rule violation)
- `404`: Node not found
- `422`: Validation Error

---

## `DELETE /node/{node_id}`

**Summary**: Delete Node  
**Method**: DELETE  
**Path Parameter**:
- `node_id` (UUID)

**Responses**:
- `204`: Success (No Content)
- `404`: Node not found
- `422`: Validation Error
