from vector_search import CourseVectorSearch
import time



search_engine = CourseVectorSearch()
# only for the first time
# search_engine.create_collection()
# search_engine.load_and_prepare_data()


# search_engine.create_collection()
# search_engine.upload_to_qdrant()

role = 'Data Analytic'
skills = ['python', 'c++', 'docker']
query = "I want to learn data analysis and earn more money"

start_time = time.time()
title_vec, desc_vec, skills_vec = search_engine.encode_query(role, query, skills)
results = search_engine.search_courses_batch_weighted(title_vec, desc_vec, skills_vec)

end_time = time.time()
execution_time = end_time - start_time

for item in results:
    print(f"Course ID: {item['details']['id']}")
    print(f"Title: {item['details']['title']}")
    print(f"Weighted score: {item['weighted_score']:.4f}")
    print(f"Original_scores: {item['details']['original_scores']}")
    print(f"Course Info: {item['details']['original_point']}")
    print('---')

print(f"{execution_time*1000:.4f} ms")

