import pandas as pd
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, NamedVector, SearchRequest
from collections import defaultdict

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


class CourseVectorSearch:
    #todo: make model downloading, data downloading and vectorizing only once
    def __init__(self, csv_path='courses_final.csv', collection_name='courses', qdrant_host='localhost', qdrant_port=6333):
        logger.info("Initialization CourseVectorSearch")
        self.collection_name = collection_name
        self.skills_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        self.client = QdrantClient(host=qdrant_host, port=qdrant_port)

        logger.info(f"Download data from {csv_path}")
        self.df = pd.read_csv(csv_path)
        self._prepare_vectors()
        self.qdrant_data = [self._prepare_for_qdrant(row) for _, row in self.df.iterrows()]

    def _prepare_vectors(self):
        logger.info("deleting NaNs")
        self.df = self.df.dropna(subset=["title", "description", "skills"]).reset_index(drop=True)
        logger.info("vectorizing cources...")
        self.df["vectors"] = self.df.apply(self._vectorize, axis=1)
        logger.info("vectorization completed")

    def _vectorize(self, row):
        return {
            "title_vector": self.skills_model.encode(row["title"], show_progress_bar=False),
            "desc_vector": self.skills_model.encode(row["description"], show_progress_bar=False),
            "skills_vector": self.skills_model.encode(", ".join(row["skills"]), show_progress_bar=False)
        }
    # todo: make better?
    def _prepare_for_qdrant(self, row):
        row_id = int(row.name)
        return {
            "id": row_id,
            "vector": {
                "title": row["vectors"]["title_vector"].tolist(),
                "description": row["vectors"]["desc_vector"].tolist(),
                "skills": row["vectors"]["skills_vector"].tolist()
            },
            "payload": {
                "title": row["title"],
                "skills": row["skills"],
                "difficulty": row["difficulty"],
                "rating": float(row["rating"])
            }
        }

    def create_collection(self):
        logger.info(f"check if colletion exists '{self.collection_name}'")
        if self.client.collection_exists(self.collection_name):
            logger.info(f"deleting collection '{self.collection_name}'")
            self.client.delete_collection(self.collection_name)
        logger.info(f"Creating new collection '{self.collection_name}'")
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config={
                "title": VectorParams(size=384, distance=Distance.COSINE),
                "description": VectorParams(size=384, distance=Distance.COSINE),
                "skills": VectorParams(size=384, distance=Distance.COSINE)
            }
        )

    def upload_to_qdrant(self):
        logger.info(f"uploading {len(self.qdrant_data)} points to Qdrant")
        points = [
            PointStruct(
                id=item["id"],
                vector=item["vector"],
                payload=item["payload"]
            )
            for item in self.qdrant_data
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)
        logger.info("uploading completed")

    def encode_query(self, role, query, skills):
        logger.info("vectorizing user query")
        return (
            self.skills_model.encode(role),
            self.skills_model.encode(query),
            self.skills_model.encode(", ".join(skills))
        )

    def search_courses_batch_weighted(self, title_vector, description_vector, skills_vector,
                                      weights={'title': 0.3, 'description': 0.2, 'skills': 0.5}, limit=5):
        logger.info("searching courses batch weighted")
        search_requests = [
            SearchRequest(vector=NamedVector(name="title", vector=title_vector), limit=40, with_payload=True),
            SearchRequest(vector=NamedVector(name="description", vector=description_vector), limit=40, with_payload=True),
            SearchRequest(vector=NamedVector(name="skills", vector=skills_vector), limit=40, with_payload=True)
        ]
        batch_results = self.client.search_batch(
            collection_name=self.collection_name,
            requests=search_requests
        )

        weighted_scores = defaultdict(lambda: {
            'weighted_score': 0,
            'point': None,
            'original_scores': {'title': 0, 'description': 0, 'skills': 0}
        })
        logger.info("summing up and weighting searching results")

        vector_names = ['title', 'description', 'skills']
        for i, results in enumerate(batch_results):
            vector_name = vector_names[i]
            weight = weights[vector_name]
            for point in results:
                if point.id not in weighted_scores:
                    weighted_scores[point.id]['point'] = point
                weighted_scores[point.id]['weighted_score'] += point.score * weight
                weighted_scores[point.id]['original_scores'][vector_name] = point.score

        sorted_results = sorted(weighted_scores.values(), key=lambda x: x['weighted_score'], reverse=True)

        logger.info(f"chosed {len(sorted_results[:limit])} best courses")

        return [
            {
                "point": item['point'],
                "weighted_score": item['weighted_score'],
                "details": {
                    "id": item['point'].id,
                    "title": item['point'].payload.get('title'),
                    "original_scores": item["original_scores"],
                    "original_point": item["point"].payload
                }
            }
            for item in sorted_results[:limit]
        ]


