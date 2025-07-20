import csv
import uuid
import psycopg2
import ast
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from itertools import islice

embedding_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# To run this script insert your cridentials in corresponding fields

# --- 1. Connect to PostgreSQL ---
pg_conn = psycopg2.connect(
    dbname="db",
    user="user",
    password="password",
    host="10",
    port="5432"
)
pg_cur = pg_conn.cursor()

# --- 2. Connect to Qdrant ---
qdrant = QdrantClient(
    url="h333", 
    api_key="e",
)

# --- 4. Create Qdrant Collection with Named Vectors ---
qdrant.recreate_collection(
    collection_name="courses",
    vectors_config={
        "title": VectorParams(size=384, distance=Distance.COSINE),
        "description": VectorParams(size=384, distance=Distance.COSINE),
        "skills": VectorParams(size=384, distance=Distance.COSINE),
    }
)

# --- Read and insert from CSV ---
points = []
with open('courses_final.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        resource_id = uuid.uuid4()

        # Extract and clean fields
        title = row['title']
        summary = row['description']
        content = row['url']
        level = row['difficulty']
        if level not in ['Beginner', 'Intermediate', 'Advanced']:
            level = 'Beginner'
        price = float(row['price']) if row['price'] else 0.0
        platform = row['source']
        rating = float(row['rating']) if row['rating'] else 5,0
        skills = ast.literal_eval(row['skills']) if row['skills'] else []
        print("Inserting resource: ", title)
        # --- INSERT INTO POSTGRES ---
        pg_cur.execute("""
            INSERT INTO resource (
                resource_id, resource_type, title, summary, content, level,
                price, platform, rating, language, duration_hours,
                published_date, certificate_available, skills_covered
            )
            VALUES (
                %s, 'Course', %s, %s, %s, %s,
                %s, %s, %s, 'English', NULL,
                NULL, FALSE, %s
            )
        """, (
            str(resource_id), title, summary, content, level,
            price, platform, rating, skills
        ))

        # --- QDRANT VECTORS ---
        title_vec = embedding_model.encode(title or "")
        desc_vec = embedding_model.encode(summary or "")
        skills_vec = embedding_model.encode(", ".join(skills))

        points.append(PointStruct(
            id=str(resource_id),
            vector={
                "title": title_vec,
                "description": desc_vec,
                "skills": skills_vec
            },
            payload={
                "title": title,
                "description": summary,
                "skills": skills
            }
        ))

# Commit Postgres inserts
pg_conn.commit()

# Insert into Qdrant

def batched(iterable, n):
    it = iter(iterable)
    while batch := list(islice(it, n)):
        yield batch

for batch in batched(points, 50):
    qdrant.upsert(collection_name="courses", points=batch)


# Clean up
pg_cur.close()
pg_conn.close()
