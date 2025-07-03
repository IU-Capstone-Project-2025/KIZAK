# KIZAK Course Recommendation (ML Module)

This module is part of the KIZAK project and is responsible for recommending courses based on a user’s missing skills, interests, and target profession. It combines vector search, skill gap analysis, and course ranking.

## 🔧 Technologies Used

- 🧠 SentenceTransformer — for generating semantic embeddings of courses and user queries
- 🗃 Qdrant — stores and indexes course vectors for fast semantic search
- 📦 JSON — stores profession-to-skills mapping
- 🧹 nltk — removes stop words
- ✂️ scikit-learn (CountVectorizer, TF-IDF, KMeans) — used for bigrams, vectorization, and clustering
- 🔁 spacy — removes duplicates using NLP techniques

## 📁 Project Structure

Only the ml/ folder is relevant to the ML module. Other directories are part of the full-stack project.

```

ml/
├── course_recommender.py         # Main script (asks for user input and displays course recommendations)
├── vector_search.py              # Handles vector search using Qdrant
├── ranker.py                     # Course ranking algorithm and ranking evaluation
├── skipGapAnalyzer.py            # Identifies user's missing skills
├── job_skill.json                # Mapping: profession → skills
├── courses_final.csv             # Dataset of courses and their associated skills
├── multi-platform-online-courses-dataset/ # Intermediate mapping datasets
├── embedding_generator.ipynb      # Used for generating embeddings and preprocessing courses
├── jv_mapping.ipynb               # Builds profession-skill mapping from job datasets
└── qdrant/                        # (created manually) stores local Qdrant vector database

````

## 🚀 How to Run

1. Navigate to the ml folder:
   ```bash
   cd ml
   ```

2. Create a qdrant folder inside:

   ```bash
   mkdir qdrant
   ```

3. Run Qdrant in docker from project root for the first time (only once):

   ```bash
   docker run -d -p 6333:6333 -v ml/qdrant:/qdrant_storage --name qd qdrant/qdrant
   ```

4. For subsequent runs, restart the container:

   ```bash
   docker restart qd
   ```

5. Run the recommendation script:

   ```bash
   python course_recommender.py
   ```

The script will ask:

* What is user's target job (e.g., python developer)
* What are user's current skills (comma-separated)
* A free-form query: what and why user want to learn something

It will then display:

* User skill gap for target job
* Top courses found via vector search
* Final ranked recommendations

## 📝 Example

```
What is user's target vacancy?:
>>> python developer

Enter user's current skills, separated by comma:
>>> python, docker

Enter user's query (what they want to learn, why, etc.):
>>> java
```

## 📄 License

MIT License

