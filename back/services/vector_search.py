from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import NamedVector, SearchRequest
from collections import defaultdict
import torch
import os

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


class CourseVectorSearch:
    def __init__(self):
        self._init_qdrant()
        self._init_embedder()
        
    def _init_qdrant(self, collection_name: str='courses', debug: bool = False) -> None:       
        logger.info("Initializing QDrant connection")
        self.client = QdrantClient(
            url=os.getenv("QD_URL"),
            api_key=os.getenv("QD_API_KEY")
        )
        logger.info("Connected successfully")
        self.collection_name = collection_name

    def _init_embedder(self, model='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', max_seq=512, use_gpu=True) -> None:
        self.device = 'cuda' if torch.cuda.is_available() and use_gpu else 'cpu'
        logger.info("Set device to %s", self.device)
        
        self.skills_model = SentenceTransformer(model)
        logger.info("Loaded %s model", model)
        self.skills_model.max_seq_length = max_seq
        
    def get_courses(self, user_role, user_query, user_skills):
        logger.info("Vectorizing user data")
        logger.info("Searching for best courses")
        results = self.search_courses_batch_weighted(
            self.skills_model.encode(user_role),
            self.skills_model.encode(user_query),
            self.skills_model.encode(", ".join(user_skills))
        )
        return results

    def search_courses_batch_weighted(self, title_vector, description_vector, skills_vector,
                                      weights={'title': 0.2, 'description': 0.1, 'skills': 0.7}, limit=50):
        logger.info("Searching courses batch weighted")
        search_requests = [
            SearchRequest(vector=NamedVector(name="title", vector=title_vector), limit=50, with_payload=True),
            SearchRequest(vector=NamedVector(name="description", vector=description_vector), limit=20, with_payload=True),
            SearchRequest(vector=NamedVector(name="skills", vector=skills_vector), limit=100, with_payload=True)
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
        logger.info("Summing up and weighting searching results")

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

        logger.info(f"Chosen {len(sorted_results[:limit])} best courses")

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


