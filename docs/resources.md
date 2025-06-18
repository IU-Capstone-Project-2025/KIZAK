# Resource API

## `GET /resource/{res_id}`

**Summary**: Get Resource  
**Path Parameter**:
- `res_id` (UUID)  
**Responses**:
- `200`: `ResourceResponse`
- `422`: Validation Error

## `POST /resource/`

**Summary**: Post Resource  
**Body**: `ResourceCreate`  
**Responses**:
- `200`: `ResourceResponse`
- `422`: Validation Error

## `PUT /resource/`

**Summary**: Put Resource  
**Body**: `ResourceUpdate`  
**Responses**:
- `200`: `ResourceResponse`
- `422`: Validation Error

## `DELETE /resource/{res_id}`

**Summary**: Delete Resource  
**Path Parameter**:
- `res_id` (UUID)  
**Responses**:
- `200`: Success
- `422`: Validation Error
