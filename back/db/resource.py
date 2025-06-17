from .db_connector import get_conn
from uuid import UUID
from models.resource import ResourceResponse, ResourseCreate, ResourceUpdate

async def retrive_resource(res_id: UUID) -> ResourceResponse:
    """Finds resource based on given res_id

    Args:
        res_id (UUID): Resource id

    Returns:
        ResourceResponse (ResourceResponse): Result
    """
    async with await get_conn() as conn:
        row = await conn.fetchrow("""
            SELECT
                resource_id,
                resource_type,
                title,
                summary,
                summary_vector,
                content,
                level,
                price,
                language,
                duration_hours,
                platform,
                rating,
                published_date,
                certificate_available,
                skills_covered,
                skills_covered_vector
            FROM resource
            WHERE resource_id = $1
        """, res_id)
        resource = ResourceResponse(**row)

        return resource
    
async def create_resource(res: ResourseCreate) -> ResourceResponse:
    """Creates a new learning resource in the database.
    
    Args:
        res: ResourceCreate object containing resource data (without ID)
        
    Returns:
        ResourceResponse: The newly created resource with all fields including generated ID
        
    Raises:
        ValueError: If insertion fails or no data is returned
        Exception: For database errors
    """
    async with await get_conn() as conn:
        async with conn.transaction():
            row = await conn.fetchrow("""
                INSERT INTO resource (
                    resource_type,
                    title,
                    summary,
                    summary_vector,
                    content,
                    level,
                    price,
                    language,
                    duration_hours,
                    platform,
                    rating,
                    published_date,
                    certificate_available,
                    skills_covered,
                    skills_covered_vector
                )
                VALUES ($1, $2, $3, $4, $5, $6,
                       $7, $8, $9, $10, $11, $12,
                       $13, $14, $15)
                RETURNING *
            """,
            res.resource_type,
            res.title,
            res.summary,
            res.content,
            res.level,
            res.price,
            res.language,
            res.duration_hours,
            res.platform,
            res.rating,
            res.published_date,
            res.certificate_available,
            res.skills_covered,
            )

            return ResourceResponse(**row)

async def update_resource(res: ResourceUpdate) -> ResourceResponse:
    """Updates an existing resource with partial data.
    
    Only updates fields that are provided (non-None values).
    The resource_id is required and identifies which resource to update.

    Args:
        res: ResourceUpdate object containing fields to update

    Returns:
        The complete updated resource with all fields

    Raises:
        ValueError: If no resource exists with the given ID
        Exception: For database errors during update
    """
    async with await get_conn() as conn:
        async with conn.transaction():
            updates = []
            values = []
            field_index = 1
            
            if res.resource_type is not None:
                updates.append(f"resource_type = ${field_index}")
                values.append(res.resource_type)
                field_index += 1
            if res.title is not None:
                updates.append(f"title = ${field_index}")
                values.append(res.title)
                field_index += 1
            if res.summary is not None:
                updates.append(f"summary = ${field_index}")
                values.append(res.summary)
                field_index += 1
            if res.content is not None:
                updates.append(f"content = ${field_index}")
                values.append(res.content)
                field_index += 1
            if res.level is not None:
                updates.append(f"level = ${field_index}")
                values.append(res.level)
                field_index += 1
            if res.price is not None:
                updates.append(f"price = ${field_index}")
                values.append(res.price)
                field_index += 1
            if res.language is not None:
                updates.append(f"language = ${field_index}")
                values.append(res.language)
                field_index += 1
            if res.duration_hours is not None:
                updates.append(f"duration_hours = ${field_index}")
                values.append(res.duration_hours)
                field_index += 1
            if res.platform is not None:
                updates.append(f"platform = ${field_index}")
                values.append(res.platform)
                field_index += 1
            if res.rating is not None:
                updates.append(f"rating = ${field_index}")
                values.append(res.rating)
                field_index += 1
            if res.published_date is not None:
                updates.append(f"published_date = ${field_index}")
                values.append(res.published_date)
                field_index += 1
            if res.certificate_available is not None:
                updates.append(f"certificate_available = ${field_index}")
                values.append(res.certificate_available)
                field_index += 1
            if res.skills_covered is not None:
                updates.append(f"skills_covered = ${field_index}")
                values.append(res.skills_covered)
                field_index += 1

            values.append(res.resource_id)

            if not updates:
                raise ValueError("No fields provided for update")

            query = f"""
                UPDATE resource
                SET {', '.join(updates)}
                WHERE resource_id = ${field_index}
                RETURNING *
            """

            row = await conn.fetchrow(query, *values)
            
            if not row:
                raise ValueError(f"No resource found with id {res.resource_id}")

            return ResourceResponse(**row)
        
async def remove_resource(res_id: UUID) -> None:
    """Deletes a resource from the database.
    
    Args:
        res_id: UUID of the resource to delete
        
    Raises:
        ValueError: If no resource exists with the given ID
        Exception: For database errors during deletion
    """
    async with await get_conn() as conn:
        async with conn.transaction():
            await conn.execute(
                """
                DELETE FROM resource 
                WHERE resource_id = $1
                """,
                res_id
            )
