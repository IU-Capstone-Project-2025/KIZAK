from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import NamedVector, SearchRequest
from qdrant_client.http.models import QueryRequest, NamedVector
from qdrant_client.models import SearchRequest, NamedVector, Batch, Query
from collections import defaultdict
import torch
import os
import json
import pandas as pd
import accessify
import re
import requests

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

class CourseDataProcessor:
    def __init__(self, json_path, csv_path, mapping_path=None):
        self.json_path = json_path
        self.csv_path = csv_path
        self.mapping_path = mapping_path
        self.mapping = {}
        self.courses = pd.DataFrame()


    def load_json(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        self.courses = pd.DataFrame(raw_data)
        logger.info(f"Read data from {self.json_path}")

    def clean_skill(self, skill: str) -> str:
        skill = skill.lower()
        skill = re.sub(r'#+', '', skill)
        skill = skill.replace("-", " ")
        skill = re.sub(r'\s+', ' ', skill)
        skill = re.sub(r'[^\w\s]', '', skill)
        return skill.strip()

    def clean_skills(self, cell: str) -> str:
        skills = [self.clean_skill(s) for s in cell.split(",")]
        logger.info(f"Perform skills to normal form")
        return ", ".join(skills)

    def apply_mapping(self):
        if not self.mapping_path:
            return
        with open(self.mapping_path, 'r', encoding='utf-8') as f:
            self.mapping = json.load(f)

        for column, replace_map in self.mapping.items():
            if column in self.courses.columns:
                self.courses[column] = self.courses[column].replace(replace_map)

        logger.info(f"Apply mapping for skills using {self.mapping_path}")

    def check_invalid_links(self):
        invalid_urls = []

        for course_url in self.courses['url']:
            try:
                print(f"Checking: {course_url}")
                response = requests.head(course_url, allow_redirects=True, timeout=25)
                if response.status_code >= 400:
                    invalid_urls.append(course_url)
            except Exception as e:
                invalid_urls.append(course_url)

        self.courses = self.courses[~self.courses['url'].isin(invalid_urls)]
        logger.info(f"Clean from invalid url")

    def run(self):
        self.load_json()
        self.apply_mapping()
        self.courses['skills'] = self.courses['skills'].apply(self.clean_skills)
        self.export_to_csv()


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
        logger.info(f"QDrant URL: {os.getenv('QD_URL')}")
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
                                      weights={'title': 0.2, 'description': 0.1, 'skills': 0.7}, limit=30):

        try:
            # to tast connection
            self.client.get_collection(self.collection_name)
        except Exception as e:
            logger.error(f"Collection access error: {str(e)}")
            raise

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

        # search_requests = [
        #     SearchRequest(
        #         vector=NamedVector(name="title", vector=title_vector),
        #         limit=50,
        #         with_payload=True
        #     ),
        #     SearchRequest(
        #         vector=NamedVector(name="description", vector=description_vector),
        #         limit=20,
        #         with_payload=True
        #     ),
        #     SearchRequest(
        #         vector=NamedVector(name="skills", vector=skills_vector),
        #         limit=100,
        #         with_payload=True
        #     )
        # ]
        #
        # batch_results = self.client.query_batch_points(
        #     collection_name=self.collection_name,
        #     requests=search_requests
        # )

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

        # example_course = {
        #     "point": sorted_results[0]['point'],
        #     "weighted_score": sorted_results[0]['weighted_score'],
        #     "details": {
        #         "id": sorted_results[0]['point'].id,
        #         "title": sorted_results[0]['point'].payload.get('title'),
        #         "original_scores": sorted_results[0]["original_scores"],
        #         "original_point": sorted_results[0]["point"].payload
        #     }
        # }
        # logger.info(f"Example returned course: {example_course}")

        return [
            {
                "point": item['point'],
                "weighted_score": item['weighted_score'],
                "details": {
                    "id": item['point'].id,
                    "title": item['point'].payload.get('title'),
                    "original_scores": item["original_scores"],
                    "original_point": {
                        "title": item['point'].payload.get("title"),
                        "skills": item['point'].payload.get("skills", []),
                        "rating": item['point'].payload.get("rating", 0),
                        "price": item['point'].payload.get("price", 0),
                        "author": item['point'].payload.get("author")
                    }
                }
            }
            for item in sorted_results[:limit]
        ]



