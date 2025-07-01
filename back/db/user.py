from typing import Any
from uuid import UUID

from utils.logger import logger

from fastapi import HTTPException
from models.user import UserCreate, UserResponse, UserUpdate, UserSkill, UserPassword

from db.db_connector import db


from fastapi import HTTPException, status


async def create_user(user: UserCreate) -> UserResponse:
    try:
        async with db.transaction() as conn:
            logger.info(f"Inserting {user.login} to users table")
            user_response = await conn.fetchrow(
                """
                    INSERT INTO users (
                        login,
                        password,
                        background,
                        education,
                        goals,
                        goal_vacancy
                    )
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
                logger.error(f"Failed to insert {user.login} to users table")
                raise HTTPException(
                    status_code=500, detail="Failed to create user"
                )
            logger.info(f"Inserted {user.login} to users table")

            records = [
                (user_response["user_id"], skill.skill,
                 skill.skill_level, skill.is_goal)
                for skill in user.skills
            ]

            logger.info(
                f"Inserting {user.login}'s skills to user_skills table"
            )
            await conn.executemany(
                """
                INSERT INTO user_skills (
                    user_id,
                    skill,
                    skill_level,
                    is_goal
                )
                VALUES ($1, $2, $3, $4)
                """,
                records
            )
            logger.info(f"Inserted {user.login}'s skills to user_skills table")
        logger.info(f"User {user.login} successfully created")
        return UserResponse(**user_response, skills=user.skills)
    except Exception:
        raise


async def retrieve_user(user_id: UUID) -> UserResponse:
    try:
        async with db.transaction() as conn:
            user_response = await conn.fetchrow(
                """
                    SELECT
                        users.user_id,
                        users.login,
                        users.password,
                        users.creation_date,
                        users.background,
                        users.education,
                        users.goals,
                        users.goal_vacancy
                    FROM users
                    WHERE users.user_id = $1
                """,
                user_id
            )

            skills_response = await conn.fetch(
                """
                    SELECT skill, skill_level, is_goal
                    FROM user_skills
                    WHERE user_id = $1
                """,
                user_id
            )

            skills = [UserSkill(**s) for s in skills_response]

            if not user_response:
                logger.error(f"Failed to retrieve user {user_id}")
                raise HTTPException(
                    status_code=404, detail="Failed to retrieve user"
                )
            logger.info(f"User {user_id} retrieved successfully")
            return UserResponse(**user_response, skills=skills)
    except Exception:
        raise


async def update_user(user: UserUpdate) -> UserResponse:
    try:
        async with db.transaction() as conn:
            updated = False

            user_exists = await conn.fetchrow(
                """
                    SELECT 1 FROM users WHERE user_id = $1
                """,
                user.user_id,
            )

            if not user_exists:
                logger.error(f"User {user.user_id} does not exist")
                raise HTTPException(
                    status_code=404,
                    detail=f"User not found with id {user.user_id}",
                )

            if user.skills is not None:
                logger.info(f"Updating {user.user_id} skills")
                await conn.execute(
                    """
                DELETE FROM user_skills WHERE user_id = $1
                """,
                    user.user_id,
                )

                records = [
                    (user.user_id, skill.skill,
                     skill.skill_level, skill.is_goal)
                    for skill in user.skills
                ]
                await conn.executemany(
                    """
                    INSERT INTO user_skills (
                        user_id,
                        skill,
                        skill_level,
                        is_goal)
                    VALUES ($1, $2, $3, $4)
                    """,
                    records
                )
                logger.info(f"Updated {user.user_id} new skills")

                updated = True

            users_update_fields = {}

            if user.login is not None:
                users_update_fields["login"] = user.login
            if user.password is not None:
                users_update_fields["password"] = user.password
            if user.background is not None:
                users_update_fields["background"] = user.background
            if user.education is not None:
                users_update_fields["education"] = user.education
            if user.goals is not None:
                users_update_fields["goals"] = user.goals
            if user.goal_vacancy is not None:
                users_update_fields["goal_vacancy"] = user.goal_vacancy

            if users_update_fields:
                await _update("users", users_update_fields, user.user_id, conn)
                updated = True

            if not updated:
                logger.error(
                    f"User {user.user_id}: No fields provided for update"
                )
                raise HTTPException(
                    status_code=400, detail="No fields provided for update"
                )

            user_response = await conn.fetchrow(
                """
                    SELECT
                        users.user_id,
                        users.login,
                        users.password,
                        users.creation_date,
                        users.background,
                        users.education,
                        users.goals,
                        users.goal_vacancy
                    FROM users
                    WHERE users.user_id = $1
                """,
                user.user_id
            )

            skills_response = await conn.fetch(
                """
                    SELECT skill, skill_level, is_goal
                    FROM user_skills
                    WHERE user_id = $1
                """,
                user.user_id
            )

            skills = [UserSkill(**s) for s in skills_response]

            return UserResponse(**user_response, skills=skills)
    except Exception:
        raise


async def remove_user(user_id: UUID) -> None:
    try:
        async with db.transaction() as conn:
            logger.info(f"Removing user {user_id}")
            result = await conn.execute(
                """
                DELETE FROM users
                WHERE user_id = $1
                """,
                user_id,
            )

            if result == "DELETE 0":
                logger.error(f"Failed to remove user {user_id}")
                raise HTTPException(status_code=404,
                                    detail="Resource not found")
    except Exception:
        raise


async def _update(table: str, fields: dict[str, Any], user_id: UUID,
                  conn) -> bool:

    logger.info(f"Updating {user_id} user fields {', '.join(fields.keys())}")
    values = list(fields.values()) + [user_id]

    query = f"""
    UPDATE {table}
    SET {', '.join([f"{field} = ${i + 1}" for i, field in enumerate(fields)])}
    WHERE user_id = ${len(values)}
    RETURNING *
    """

    res = await conn.fetchrow(query, *values)

    if not res:
        logger.error(
            f"""
            Failed to update user {user_id} fields {', '.join(fields.keys())}
            """
        )
        raise HTTPException(
            status_code=500, detail=f"Failed to update fields in {table}"
        )
    logger.info(f"Updated {user_id} user fields {', '.join(fields.keys())}")
    return True




async def get_user_from_db(login: str) -> UserPassword:
    if not isinstance(login, str):
        raise TypeError(f"Login must be a string, got {type(login).__name__}")


    try:
        user_response = await db.fetchrow(
            """
                SELECT
                    users.user_id,
                    users.login,
                    users.password, 
                    users.creation_date
                FROM users
                WHERE users.login = $1
            """,
            login
        )


        if not user_response:
            logger.error(f"Failed to retrieve user {login}")
            raise HTTPException(
                status_code=404, detail="Failed to retrieve user"
            )
        logger.info(f"User {login} retrieved successfully")
        return UserPassword(**user_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



async def get_userResp_from_db(login: str) -> UserResponse:
    if not isinstance(login, str):
        raise TypeError(f"Login must be a string, got {type(login).__name__}")


    try:
        user_response = await db.fetchrow(
            """
                SELECT
                    users.user_id,
                    users.creation_date
                FROM users
                WHERE users.login = $1
            """,
            login
        )


        if not user_response:
            logger.error(f"Failed to retrieve user {login}")
            raise HTTPException(
                status_code=404, detail="Failed to retrieve user"
            )
        logger.info(f"User {login} retrieved successfully")
        return UserResponse(**user_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
