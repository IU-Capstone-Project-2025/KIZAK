from flask import request
from flask_restful import Resource
from datetime import datetime
from sentence_transformers import SentenceTransformer

from ..db.connect import get_db_connection


def create_vector(text):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    vector = model.encode(text)
    return vector.tolist()


class UserAPI(Resource):
    async def get(self, user_id):
        conn = await get_db_connection()

        user_row = await conn.fetchrow(f"SELECT login, password, creation_date FROM users WHERE id = {user_id}")

        if not user_row:
            await conn.close()
            return {'error': 'User not found'}, 404

        data = {
            "id": user_id,
            "login": user_row[0],
            "password": user_row[1],
            "creation_date": user_row[2],
        }

        user_profile_row = await conn.fetchrow(
            f"SELECT background, goals, goal_vacancy FROM user_profiles WHERE id = {user_id}")

        data["background"] = user_profile_row[0]
        data["goals"] = user_profile_row[1]
        data["goal_vacancy"] = user_profile_row[2]

        user_skills_row = await conn.fetch(f"SELECT skill, skill_level FROM user_skills WHERE user_id = {user_id}")

        data["skills"] = [row[0] for row in user_skills_row]
        data["skills_levels"] = [row[1] for row in user_skills_row]

        user_goals_row = await conn.fetch(f"SELECT goal FROM user_goals WHERE user_id = {user_id}")
        data["goal_skills"] = [row[0] for row in user_goals_row]

        await conn.close()

        return data, 200

    async def post(self):
        data = request.get_json()

        conn = await get_db_connection()

        login = data['login']
        password = data['password']
        timestamp = datetime.now()
        background = data['background']
        background_vector = create_vector(background)
        education = data['education']
        skills = data['skills']
        skills_levels = data['skills_levels']
        goal_skills = data['goal_skills']
        goals = data['goals']
        goals_vector = create_vector(goals)
        goal_vacancy = data['goal_vacancy']
        goal_vacancy_vector = create_vector(goal_vacancy)

        result = await conn.fetchrow(f'''
        INSERT INTO users (login, password, creation_date) VALUES ({login}, {password}, {timestamp}) RETURNING id;
        ''')

        user_id = result['id']

        await conn.execute(f'''
        INSERT INTO user_profiles (id, background, background_vector, goals, goals_vector, goal_vacancy, goal_vacancy_vector) VALUES ({user_id}, {background}, {background_vector},{goals}, {goals_vector}, {goal_vacancy}, {goal_vacancy_vector});
        ''')

        for i in range(len(skills)):
            skill = skills[i]
            skill_vector = create_vector(skill)
            level = skills_levels[i]
            level_vector = create_vector(level)

            await conn.execute(f'''
            INSERT INTO user_skills (user_id, skill, skill_vector, skill_level, level_vector) VALUES ({user_id}, {skill}, {skill_vector}, {level}, {level_vector});
            ''')

        for goal_skill in goal_skills:
            goal_skill_vector = create_vector(goal_skill)

            await conn.execute(f'''
            INSERT INTO user_goals (user_id, goal, goal_vector) VALUES ({user_id}, {goal_skill}, {goal_skill_vector});
            ''')

        await conn.close()
        return {"message": "User created",
                "user_id": user_id}, 201

    async def delete(self, user_id):

        conn = await get_db_connection()

        await conn.execute(f"DELETE FROM users WHERE id = {user_id};")

        await conn.close()

        return {"message": f"User deleted",
                "user_id": user_id}, 200

    async def put(self, user_id):
        data = request.get_json()
        conn = await get_db_connection()

        if 'skills' in data and 'skills_levels' in data:
            skills = data['skills']
            skills_levels = data['skills_levels']

            if len(skills) != len(skills_levels):
                await conn.close()
                return {"error": "skills and skills_levels length mismatch"}, 400

            await conn.execute(f"DELETE FROM user_skills WHERE user_id = {user_id};")

            for i in range(len(skills)):
                skill = skills[i]
                skill_vector = create_vector(skill)
                level = skills_levels[i]
                level_vector = create_vector(level)

                await conn.execute(f'''
                INSERT INTO user_skills (user_id, skill, skill_vector, skill_level, level_vector) VALUES ({user_id}, {skill}, {skill_vector}, {level}, {level_vector});
                ''')

        if 'login' in data:
            login = data['login']
            await conn.execute(f'UPDATE users SET login = {login} WHERE id = {user_id};')

        if 'password' in data:
            password = data['password']
            await conn.execute(f'UPDATE users SET password = {password} WHERE id = {user_id};')

        if 'background' in data:
            background = data['background']
            background_vector = create_vector(background)
            await conn.execute(
                f'UPDATE user_profiles SET background = {background}, background_vector = {background_vector} WHERE id = {user_id};')

        if 'goals' in data:
            goals = data['goals']
            goals_vector = create_vector(goals)
            await conn.execute(
                f'UPDATE user_profiles SET goals = {goals}, goals_vector = {goals_vector} WHERE id = {user_id};')

        if 'goal_vacancy' in data:
            goal_vacancy = data['goal_vacancy']
            goal_vacancy_vector = create_vector(goal_vacancy)
            await conn.execute(
                f'UPDATE user_profiles SET goal_vacancy = {goal_vacancy}, goal_vacancy_vector = {goal_vacancy_vector} WHERE id = {user_id};')

        if 'goal_skills' in data:
            goal_skills = data['goal_skills']
            await conn.execute(f"DELETE FROM user_goals WHERE user_id = {user_id};")

            for goal_skill in goal_skills:
                goal_skill_vector = create_vector(goal_skill)

                await conn.execute(f'''
                INSERT INTO user_goals (user_id, goal, goal_vector) VALUES ({user_id}, {goal_skill}, {goal_skill_vector});
                ''')

        await conn.close()

        return {"message": "User updated", "user_id": user_id, "new data": data}, 200
