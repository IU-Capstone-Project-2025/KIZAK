from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from utils.logger import logger

from fastapi import HTTPException
from models.user import UserCreate, UserResponse, UserUpdate

from .db_connector import db


async def create_user(user: UserCreate) -> UserResponse:
    try:
        async with db.transaction():
            await _check_len(user.skills, user.skills_levels)

            logger.info(f"Inserting {user.login} to users table")
            user_response = await db.fetchrow(
                """
            INSERT INTO users (login, password, creation_date)
            VALUES ($1, $2, $3)
            RETURNING *
            """,
                user.login,
                user.password,
                datetime.now(),
            )

            if not user_response:
                logger.error(f"Failed to insert {user.login} to users table")
                raise HTTPException(
                    status_code=500, detail="Failed to create user"
                )
            logger.info(f"Inserted {user.login} to users table")

            logger.info(f"Inserting {user.login} to users_profiles table")
            user_profile_response = await db.fetchrow(
                """
            INSERT INTO user_profiles
            (user_id, background, goals, goal_vacancy, education)
            VALUES  ($1, $2, $3, $4, $5)
            RETURNING background, goals, goal_vacancy, education
            """,
                user_response["user_id"],
                user.background,
                user.goals,
                user.goal_vacancy,
                user.education,
            )

            if not user_profile_response:
                logger.error(
                    f"Failed to insert {user.login} to users_profiles table"
                )
                raise HTTPException(
                    status_code=500, detail="Failed to create user profile"
                )
            logger.info(f"Inserted {user.login} to users_profiles table")

            records = [
                (user_response["user_id"], skill, level)
                for skill, level in zip(user.skills, user.skills_levels)
            ]

            logger.info(
                f"Inserting {user.login}'s skills to user_skills table"
            )
            await db.executemany(
                """
                INSERT INTO user_skills (user_id, skill, skill_level)
                VALUES ($1, $2, $3)
                """,
                records,
            )
            logger.info(f"Inserted {user.login}'s skills to user_skills table")

            goal_records = [
                (user_response["user_id"], goal) for goal in user.goal_skills
            ]

            logger.info(f"Inserting {user.login}'s goals to user_goals table")
            await db.executemany(
                """
                INSERT INTO user_goals (user_id, goal)
                VALUES ($1, $2)
                """,
                goal_records,
            )
            logger.info(f"Inserted {user.login}'s goals to user_goals table")
        logger.info(f"User {user.login} successfully created")
        return await retrieve_user(user_response["user_id"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def retrieve_user(user_id: UUID) -> UserResponse:
    try:
        user_response = await db.fetchrow(
            """
        SELECT users.user_id, users.login, users.password, users.creation_date,
         user_profiles.background, user_profiles.education,
         user_profiles.goals, user_profiles.goal_vacancy,
        COALESCE(
        (SELECT array_agg(skill ORDER BY skill)
        FROM user_skills
        WHERE user_skills.user_id = users.user_id
        ), ARRAY[]::text[]) AS skills,
        COALESCE(
        (SELECT array_agg (skill_level ORDER BY skill)
        FROM user_skills
        WHERE user_skills.user_id = users.user_id
        ), ARRAY[]::text[]) AS skills_levels,
        COALESCE(
        (SELECT array_agg (goal)
        FROM user_goals
        WHERE user_goals.user_id = users.user_id
        ), ARRAY[]::text[]) AS goal_skills
        FROM users
        JOIN user_profiles ON users.user_id = user_profiles.user_id
        WHERE users.user_id = $1
        """,
            user_id,
        )

        if not user_response:
            logger.error(f"Failed to retrieve user {user_id}")
            raise HTTPException(
                status_code=404, detail="Failed to retrieve user"
            )
        logger.info(f"User {user_id} retrieved successfully")
        return UserResponse(**user_response)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_user(user: UserUpdate) -> UserResponse:
    try:
        async with db.transaction():
            updated = False

            user_exists = await db.fetchrow(
                """
            SELECT 1 FROM users WHERE user_id = $1
            """,
                user.user_id,
            )

            if not user_exists:
                logger.error(f"User {user.user_id} does not exist")
                raise HTTPException(
                    status_code=404,
                    detail=f"Resource not found with id {user.user_id}",
                )

            if user.skills is not None and user.skills_levels is not None:
                await _check_len(user.skills, user.skills_levels)

                logger.info(f"Updating {user.user_id} skills")
                await db.execute(
                    """
                DELETE FROM user_skills WHERE user_id = $1
                """,
                    user.user_id,
                )

                records = [
                    (user.user_id, skill, level)
                    for skill, level in zip(user.skills, user.skills_levels)
                ]

                await db.executemany(
                    """
                    INSERT INTO user_skills (user_id, skill, skill_level)
                    VALUES ($1, $2, $3)
                    """,
                    records,
                )
                logger.info(f"Updated {user.user_id} new skills")

                updated = True

            elif user.skills is not None or user.skills_levels is not None:
                await _check_len(user.skills, user.skills_levels)

            if user.goal_skills is not None:
                logger.info(f"Updating {user.user_id} goals")
                await db.execute(
                    """
                DELETE FROM user_goals WHERE user_id = $1
                """,
                    user.user_id,
                )

                goal_records = [
                    (user.user_id, goal) for goal in user.goal_skills
                ]

                await db.executemany(
                    """
                    INSERT INTO user_goals (user_id, goal)
                    VALUES ($1, $2)
                    """,
                    goal_records,
                )
                logger.info(f"Updated {user.user_id} goals")

                updated = True

            users_update_fields = {}

            if user.login is not None:
                users_update_fields["login"] = user.login
            if user.password is not None:
                users_update_fields["password"] = user.password

            if users_update_fields:
                await _update("users", users_update_fields, user.user_id)
                updated = True

            profiles_update_fields = {}
            if user.background is not None:
                profiles_update_fields["background"] = user.background
            if user.education is not None:
                profiles_update_fields["education"] = user.education
            if user.goals is not None:
                profiles_update_fields["goals"] = user.goals
            if user.goal_vacancy is not None:
                profiles_update_fields["goal_vacancy"] = user.goal_vacancy

            if profiles_update_fields:
                await _update(
                    "user_profiles", profiles_update_fields, user.user_id
                )
                updated = True

            if not updated:
                logger.error(
                    f"User {user.user_id}: No fields provided for update"
                )
                raise HTTPException(
                    status_code=400, detail="No fields provided for update"
                )

            return await retrieve_user(user.user_id)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def remove_user(user_id: UUID) -> None:
    try:
        logger.info(f"Removing user {user_id}")
        result = await db.execute(
            """
            DELETE FROM users
            WHERE user_id = $1
            """,
            user_id,
        )

        if result == "DELETE 0":
            logger.error(f"Failed to remove user {user_id}")
            raise HTTPException(status_code=404, detail="Resource not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _update(table: str, fields: dict[str, Any], user_id: UUID) -> bool:
    if not fields:
        logger.error(f"No fields provided for update")
        return False

    logger.info(f"Updating {user_id} user fields {', '.join(fields.keys())}")
    values = list(fields.values()) + [user_id]

    query = f"""
    UPDATE {table}
    SET {', '.join([f"{field} = ${i + 1}" for i, field in enumerate(fields)])}
    WHERE user_id = ${len(values)}
    RETURNING *
    """

    res = await db.fetchrow(query, *values)

    if not res:
        logger.error(
            f"Failed to update user {user_id} fields {', '.join(fields.keys())}"
        )
        raise HTTPException(
            status_code=500, detail=f"Failed to update fields in {table}"
        )
    logger.info(f"Updated {user_id} user fields {', '.join(fields.keys())}")
    return True


async def _check_len(
    skills: Optional[List[str]], skills_levels: Optional[List[str]]
):
    if skills is None:
        skills = []
    if skills_levels is None:
        skills_levels = []
    if len(skills) != len(skills_levels):
        logger.error(f"Skills and skill levels count mismatch")
        raise HTTPException(
            status_code=400, detail="Skills and skill levels count mismatch"
        )
