# Node API

## `GET /node/{node_id}`

**Summary**: Get Node  
**Path Parameter**:
- `node_id` (UUID)  
**Responses**:
- `200`: `NodeResponse`
- `422`: Validation Error

## `POST /node/`

**Summary**: Post Node  
**Body**: `NodeCreate`  
**Responses**:
- `200`: `NodeResponse`
- `422`: Validation Error

## `PUT /node/`

**Summary**: Put Node  
**Body**: `NodeUpdate`  
**Responses**:
- `200`: `NodeResponse`
- `422`: Validation Error

## `DELETE /node/`

**Summary**: Delete Node  
**Query Parameter**:
- `node_id` (UUID)  
**Responses**:
- `200`: Success
- `422`: Validation Error
