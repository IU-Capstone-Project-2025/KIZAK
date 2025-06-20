from uuid import UUID

from utils.logger import logger
from db.db_connector import db
from fastapi import HTTPException
from models.resource import ResourceCreate, ResourceResponse, ResourceUpdate


async def retrieve_resource(res_id: UUID) -> ResourceResponse:
    """Finds resource based on given res_id

    Args:
        res_id (UUID): Resource id

    Returns:
        ResourceResponse: Result

    Raises:
        HTTPException: 404 if resource not found
    """
    row = await db.fetchrow(
        """
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
    """,
        res_id,
    )

    if not row:
        logger.error(f"Resource {res_id} not found")
        raise HTTPException(status_code=404, detail="Resource not found")

    logger.info(f"Retrieved resource {res_id}")

    return ResourceResponse(**row)


async def create_resource(res: ResourceCreate) -> ResourceResponse:
    """Creates a new learning resource in the database.

    Args:
        res: ResourceCreate object containing resource data

    Returns:
        ResourceResponse: The newly created resource

    Raises:
        HTTPException: 500 if database operation fails
    """
    logger.info(f"Creating new resource")
    try:
        row = await db.fetchrow(
            """
            INSERT INTO resource (
                resource_type,
                title,
                summary,
                content,
                level,
                price,
                language,
                duration_hours,
                platform,
                rating,
                published_date,
                certificate_available,
                skills_covered
            )
            VALUES ($1, $2, $3, $4, $5, $6,
                   $7, $8, $9, $10, $11, $12,
                   $13)
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

        if not row:
            logger.error(f"Failed to create resource")
            raise HTTPException(
                status_code=500, detail="Failed to create resource"
            )
        logger.debug(row)
        return ResourceResponse(**row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_resource(res: ResourceUpdate) -> ResourceResponse:
    """Updates an existing resource with partial data.

    Args:
        res: ResourceUpdate object containing fields to update

    Returns:
        ResourceResponse: The complete updated resource

    Raises:
        HTTPException: 404 if resource not found
        HTTPException: 400 if no fields provided
        HTTPException: 500 if database error occurs
    """
    try:
        updates = []
        values = []
        field_index = 1

        # Dynamically build the update query
        fields = {
            "resource_type": res.resource_type,
            "title": res.title,
            "summary": res.summary,
            "content": res.content,
            "level": res.level,
            "price": res.price,
            "language": res.language,
            "duration_hours": res.duration_hours,
            "platform": res.platform,
            "rating": res.rating,
            "published_date": res.published_date,
            "certificate_available": res.certificate_available,
            "skills_covered": res.skills_covered,
        }

        for field, value in fields.items():
            if value is not None:
                updates.append(f"{field} = ${field_index}")
                values.append(value)
                field_index += 1

        if not updates:
            logger.error(f"No fields provided for update")
            raise HTTPException(
                status_code=400, detail="No fields provided for update"
            )

        values.append(res.resource_id)
        query = f"""
            UPDATE resource
            SET {', '.join(updates)}
            WHERE resource_id = ${field_index}
            RETURNING *
        """

        row = await db.fetchrow(query, *values)

        if not row:
            logger.error(f"Resource {res.resource_id} not found")
            raise HTTPException(
                status_code=404,
                detail=f"Resource not found with id {res.resource_id}",
            )
        logger.info(f"Updated resource {res.resource_id}")
        return ResourceResponse(**row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def remove_resource(res_id: UUID) -> None:
    """Deletes a resource from the database.

    Args:
        res_id: UUID of the resource to delete

    Raises:
        HTTPException: 404 if resource not found
        HTTPException: 500 if database error occurs
    """
    try:
        result = await db.execute(
            """
            DELETE FROM resource
            WHERE resource_id = $1
            """,
            res_id,
        )

        if result == "DELETE 0":
            logger.error(f"Resource {res_id} not found")
            raise HTTPException(status_code=404, detail="Resource not found")

        logger.info(f"Deleted resource {res_id}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
