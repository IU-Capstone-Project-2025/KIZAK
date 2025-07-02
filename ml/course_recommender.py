from vector_search import CourseVectorSearch
from skipGapAnalyzer import SkillGapAnalyzer
from ranker import CourseRanker

import json
import os
#todone: try different settings to remove warnings(not working)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0 = all logs, 1 = INFO, 2 = WARNING, 3 = ERROR
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import time

with open('job_skill.json', 'r', encoding='utf-8') as f:
    job_skills_raw = json.load(f)

role_to_skills = {}
priorities_by_role = {}
for role, skills in job_skills_raw.items():
    role_to_skills[role] = [item["skill"] for item in skills]
    priorities_by_role[role] = {item["skill"]: item["priority"] for item in skills}

# user data
print("What is user's target vacancy?:")
user_role = input(">>> ").strip().lower()

print("Enter user's current skills, separated by comma:")
user_skills = [skill.strip().lower() for skill in input(">>> ").split(',')]

print("Enter user's query (what they want to learn, why, etc.):")
user_query = input(">>> ").strip()

search_engine = CourseVectorSearch()
flag_file = ".qdrant_initialized"
if not os.path.exists(flag_file):
    print("Initialization of Qdrant, uploading courses data...")
    search_engine.create_collection()
    search_engine.upload_to_qdrant()
    with open(flag_file, "w") as f:
        f.write("initialized")
else:
    print("Qdrant was previously initialized")

# analysis of user's skills, define lacking ones
gap_analyzer = SkillGapAnalyzer(role_to_skills)
gap_result = gap_analyzer.compute_gap(user_skills, user_role)
missing_skills = gap_result["missing_skills"]
print(f"\nSkill gap for '{user_role}': {missing_skills}")

start_time = time.time()

# vectorize user info
title_vec, desc_vec, skills_vec = search_engine.encode_query(user_role, user_query, user_skills)
results = search_engine.search_courses_batch_weighted(title_vec, desc_vec, skills_vec)

end_time = time.time()
execution_time = end_time - start_time

# search courses in db
search_results = search_engine.search_courses_batch_weighted(
    title_vector=title_vec,
    description_vector=desc_vec,
    skills_vector=skills_vec,
    limit=30
)
print('Time of query to vector db execution')
print(f"{execution_time*1000:.4f} ms")

# vector search results
print("\ntop-5 courses from vector search (before ranking):")
for i, res in enumerate(search_results[:5]):
    details = res['details']
    print(f"{i+1}. {details['title']} (Score: {res['weighted_score']:.4f})")
    print(f"   Skills: {details.get('original_point', {}).get('skills', [])}")
    print("---")

# convert to ranging format
courses = []
for res in search_results:
    course_info = res['details']['original_point']
    course_info['id'] = res['details']['id']
    course_info['skills'] = course_info.get('skills', [])
    course_info['rating'] = course_info.get('rating', 0)
    course_info['price'] = course_info.get('price', 0)
    courses.append(course_info)

ranker = CourseRanker(priorities_by_role)

# ranking courses
ranked_courses = ranker.rank_courses(courses, missing_skills, user_role)

# quality of ranking
metrics = ranker.evaluate_ranking(ranked_courses, missing_skills, user_role)

print("\nRecommended courses:")
for i, course in enumerate(ranked_courses[:5]):
    print(f"{i+1}. {course['course']['title']} — Score: {course['ranking_score']:.3f}")
    print(f"   Covered skills: {course['covered_skills']}")
    print(f"   Rating: {course['course'].get('rating')}")
    print("---")

print("Ranking quality metrics:", metrics)


