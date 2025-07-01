from vector_search import CourseVectorSearch

search_engine = CourseVectorSearch()
search_engine.create_collection()
search_engine.upload_to_qdrant()

role = 'Data Analytic'
skills = ['python', 'c++', 'docker']
query = "I want to learn data analysis and earn more money"

title_vec, desc_vec, skills_vec = search_engine.encode_query(role, query, skills)
results = search_engine.search_courses_batch_weighted(title_vec, desc_vec, skills_vec)

for item in results:
    print(f"Course ID: {item['details']['id']}")
    print(f"Title: {item['details']['title']}")
    print(f"Weighted score: {item['weighted_score']:.4f}")
    print(f"Original_scores: {item['details']['original_scores']}")
    print(f"Course Info: {item['details']['original_point']}")
    print('---')

