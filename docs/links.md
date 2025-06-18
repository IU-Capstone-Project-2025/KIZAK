# Link API

## `GET /link/{link_id}`

**Summary**: Get Link  
**Path Parameter**:
- `link_id` (UUID)  
**Responses**:
- `200`: `LinkResponse`
- `422`: Validation Error

## `POST /link/`

**Summary**: Post Link  
**Body**: `LinkCreate`  
**Responses**:
- `200`: `LinkResponse`
- `422`: Validation Error

## `DELETE /link/`

**Summary**: Delete Link  
**Query Parameter**:
- `link_id` (UUID)  
**Responses**:
- `200`: Success
- `422`: Validation Error
