# Scraped Courses


## Progress

Courses scraped from:

- [x] **Stepik** (~460 courses)
  - Topics:
    - Python Language
    - Machine Learning
    - Data Science
    - Backend Development

- [ ] **YouTube**

- [ ] **Coursera**


## Data Format

For now all data presented in **string** format

```json
    "title": "Title of the course",
    "course_url": "https://stepik.org/course/223532?search=7291233907",
    "author": "Jhon Doe",
    "description": "Short description of the course",
    "rating": "Rating (0-5)",
    "num_of_users": "Num of enrolled users",
    "time_to_pass": "Hours to pass the course",
    "is_certified": true,
    "price": "Price in rub",
    "skills_learned": [
      "Description of skills  !! NOT TAGS"
    ],
    "about_course": "More information about the course",
    "target_audience": "Description of target audience",
    "initial_requirements": null,
    "source": "Stepik/Coursera/YouTube"
```

## Important

**Note that for now data is raw (ie not properly processed)**
