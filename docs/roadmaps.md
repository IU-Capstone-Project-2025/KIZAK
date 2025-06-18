# Roadmap API

## `GET /roadmap/{roadmap_id}`

**Summary**: Get Roadmap  
**Path Parameter**:
- `roadmap_id` (UUID)  
**Responses**:
- `200`: `RoadmapResponse`
- `422`: Validation Error

## `POST /roadmap/`

**Summary**: Post Roadmap  
**Body**: `RoadmapCreate`  
**Responses**:
- `200`: `RoadmapResponse`
- `422`: Validation Error

## `DELETE /roadmap/{roadmap_id}`

**Summary**: Delete Roadmap  
**Path Parameter**:
- `roadmap_id` (UUID)  
**Responses**:
- `200`: Success
- `422`: Validation Error
