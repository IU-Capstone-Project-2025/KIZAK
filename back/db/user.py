from datetime import datetime
from typing import Any, List
from uuid import UUID

from fastapi import HTTPException
from models.user import UserCreate, UserResponse, UserUpdate

from .db_connector import db


async def create_user(user: UserCreate) -> UserResponse:
    try:
        async with db.transaction():
            await _check_len(user.skills, user.skills_levels)

            user_response = await db.fetchrow(
                """
            INSERT INTO users (login, password, background, education, goals, goal_vacancy)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING *
            """,
                user.login,
                user.password,
                user.background,
                user.education,
                user.goals,
                user.goal_vacancy
            )

            if not user_response:
                raise HTTPException(
                    status_code=500, detail="Failed to create user"
                )

            records = [
                (user_response["user_id"], skill, level)
                for skill, level in zip(user.skills, user.skills_levels)
            ]
            await db.executemany(
                """
                INSERT INTO user_skills (user_id, skill, skill_level)
                VALUES ($1, $2, $3)
                """,
                records,
            )

            goal_records = [
                (user_response["user_id"], goal) for goal in user.goal_skills
            ]

            await db.executemany(
                """
                INSERT INTO user_goals (user_id, goal)
                VALUES ($1, $2)
                """,
                goal_records,
            )

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
        (
        SELECT array_agg(skill ORDER BY skill)
        FROM user_skills
        WHERE user_skills.user_id = users.user_id
        ) AS skills,
        (
        SELECT array_agg (skill_level ORDER BY skill)
        FROM user_skills
        WHERE user_skills.user_id = users.user_id
        ) AS skills_levels,
        (
        SELECT array_agg (goal)
        FROM user_goals
        WHERE user_goals .user_id = users.user_id
        ) AS goal_skills
        FROM users
        JOIN user_profiles ON users.user_id = user_profiles.user_id
        WHERE users.user_id = $1
        """,
            user_id,
        )

        if not user_response:
            raise HTTPException(
                status_code=404, detail="Failed to retrieve user"
            )

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
                raise HTTPException(
                    status_code=404,
                    detail=f"Resource not found with id {user.user_id}",
                )

            if user.skills is not None and user.skills_levels is not None:
                await _check_len(user.skills, user.skills_levels)

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
                updated = True

            elif user.skills is not None or user.skills_levels is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Skills and skill levels count mismatch",
                )

            if user.goal_skills is not None:
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
        result = await db.execute(
            """
            DELETE FROM users
            WHERE user_id = $1
            """,
            user_id,
        )

        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Resource not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _update(table: str, fields: dict[str, Any], user_id: UUID) -> bool:
    if not fields:
        return False

    values = list(fields.values()) + [user_id]

    query = f"""
    UPDATE {table}
    SET {', '.join([f"{field} = ${i + 1}" for i, field in enumerate(fields)])}
    WHERE user_id = ${len(values)}
    RETURNING *
    """

    res = await db.fetchrow(query, *values)

    if not res:
        raise HTTPException(
            status_code=500, detail=f"Failed to update fields in {table}"
        )
    return True


async def _check_len(skills: List[str], skills_levels: List[str]):
    if len(skills) != len(skills_levels):
        raise HTTPException(
            status_code=400, detail="Skills and skill levels count mismatch"
        )
