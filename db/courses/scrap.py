import json
import re
from rapidfuzz import process, fuzz

official_skills = ['NumPy', 'Data Manipulation', 'File Management', 'Data Structures', 'Application Programming Interface (API)', 'Data Analysis', 'Programming Principles', 'Web Scraping', 'Restful API', 'Object Oriented Programming (OOP)', 'Computer Programming', 'Jupyter', 'Python Programming', 'Data Import/Export', 'Pandas (Python Package)', 'Development Environment', 'Computational Thinking', 'Integrated Development Environments', 'Debugging', 'Algorithms', 'Problem Management', 'Network Protocols', 'Database Design', 'SQL', 'Data Collection', 'Data Visualization Software', 'Data Processing', 'Data Modeling', 'Test Driven Development (TDD)', 'Software Testing', 'Unit Testing', 'Plotly', 'Docker (Software)', 'Scripting', 'Git (Version Control System)', 'Data Ethics', 'Agile Methodology', 'Flask (Web Framework)', 'Web Development', 'Matplotlib', 'Statistical Modeling', 'Supervised Learning', 'Predictive Modeling', 'Regression Analysis', 'Data Cleansing', 'Data Pipelines', 'Descriptive Statistics', 'Feature Engineering', 'Scikit Learn (Machine Learning Library)', 'Data Wrangling', 'Exploratory Data Analysis', 'Data-Driven Decision-Making', 'Scripting Languages', 'Image Analysis', 'Unified Modeling Language', 'Software Design', 'Object Oriented Design', 'Computer Graphics', 'Pseudocode', 'Infrastructure as Code (IaC)', 'Technical Communication', 'Cloud Computing', 'Interviewing Skills', 'Puppet (Configuration Management Tool)', 'GitHub', 'Command-Line Interface', 'Unsupervised Learning', 'Applied Machine Learning', 'Dimensionality Reduction', 'Decision Tree Learning', 'Classification And Regression Tree (CART)', 'Machine Learning', 'Query Languages', 'Databases', 'Relational Databases', 'Transaction Processing', 'Stored Procedure', 'Database Management', 'Program Development', 'Application Development', 'Data Science', 'Artificial Intelligence', 'Scientific Visualization', 'Generative AI', 'ChatGPT', 'Large Language Modeling', 'Prompt Engineering', 'Automation', 'Software Development Tools', 'Dashboard', 'Data Literacy', 'Interactive Data Visualization', 'Cybersecurity', 'Cyber Security Assessment', 'Risk Analysis', 'Financial Data', 'Statistical Inference', 'Probability & Statistics', 'Financial Trading', 'Financial Analysis', 'Statistical Analysis', 'Financial Modeling', 'Statistical Methods', 'Network Monitoring', 'Threat Detection', 'Incident Response', 'Intrusion Detection and Prevention', 'Continuous Monitoring', 'Cyber Threat Intelligence', 'Data Access', 'Cyber Threat Hunting', 'Cyber Operations', 'Computational Logic', 'Computer Science', 'Unstructured Data', 'Graph Theory', 'Network Model', 'Text Mining', 'Data Visualization', 'Scatter Plots', 'Box Plots', 'Data Presentation', 'Heat Maps', 'Seaborn', 'Geospatial Information and Technology', 'Histogram', 'User Interface (UI) Design', 'Data Mining', 'Version Control', 'Business Logic', 'Persona (User Experience)', 'Productivity', 'Ingenuity', 'Agentic systems', 'Brainstorming', 'Tensorflow', 'Verification And Validation', 'Keras (Neural Network Library)', 'Deep Learning', 'Reinforcement Learning', 'Generative AI Agents', 'Bayesian Statistics', 'Statistical Programming', 'Sampling (Statistics)', 'Tableau Software', 'Data Storytelling', 'Game Design', 'Package and Software Management', 'Software Installation', 'Data Integration', 'Java', 'Pivot Tables And Charts', 'Statistics', 'Business Analytics', 'Correlation Analysis', 'Time Series Analysis and Forecasting', 'Style Guides', 'Web Applications', 'IBM Cloud', 'Software Development Life Cycle', 'Application Deployment', 'Code Review', 'Istio', 'HTML and CSS', 'Software Architecture', 'Full-Stack Web Development', 'Django (Web Framework)', 'Kubernetes', 'Probability Distribution', 'Web Services', 'Extensible Markup Language (XML)', 'TCP/IP', 'JSON', 'Hypertext Markup Language (HTML)', 'Data Capture', 'Extract, Transform, Load', 'Google Sheets', 'Spreadsheet Software', 'Excel Formulas', 'Big Data', 'Random Forest Algorithm', 'Machine Learning Methods', 'Inventory Control', 'Information Management', 'Operations Management', 'Business Operations', 'Decision Making', 'Transportation Operations', 'Production Planning', 'Information Systems', 'Logistics', 'Software Development', 'Microsoft Development Tools', 'Software Documentation', 'Data Storage', 'Functional Testing', 'Animation and Game Design', 'Software Engineering', 'Video Game Development', 'Software Quality (SQA/SQC)', 'Test Planning', 'Bootstrap (Front-End Framework)', 'Back-End Web Development', 'Maintainability', 'Test Engineering', 'Theoretical Computer Science', 'Network Routing', 'Operations Research', 'Test Case', 'Development Testing', 'Shell Script', 'Linux Commands', 'Unix', 'Operating Systems', 'Unix Commands', 'Unix Shell', 'OS Process Management', 'Bash (Scripting Language)', 'Data Validation', 'Data Transformation', 'Professional Development', 'Engineering Software', 'Stakeholder Communications', 'Cyber Attacks', 'Computer Security Incident Management', 'Security Controls', 'Asset Management', 'Investment Management', 'Advanced Analytics', 'Financial Market', 'Portfolio Management', 'Mathematical Modeling', 'Combinatorics', 'Cryptography', 'Applied Mathematics', 'Tree Maps', 'Linear Algebra', 'Application Security', 'Selenium (Software)', 'Object-Relational Mapping', 'JavaScript Frameworks', 'Front-End Web Development', 'Vue.JS', 'Secure Coding', 'Microsoft Azure', 'Cloud Applications', 'Musical Composition', 'Music', 'Trend Analysis', 'Marketing Analytics', 'Social Media', 'Social Media Marketing', 'Natural Language Processing', 'Bioinformatics', 'Customer Analysis', 'Analytical Skills', 'Simulations', 'OpenAI', 'Artificial Intelligence and Machine Learning (AI/ML)', 'Network Security', 'MITRE ATT&CK Framework', 'IT Automation', 'Design Strategies', 'Systems Integration', 'Prototyping', 'Interoperability', 'Forecasting', 'Technical Support', 'IT Infrastructure', 'Computer Hardware', 'Applicant Tracking Systems', 'Microsoft Windows', 'Computer Security', 'Network Administration', 'Information Systems Security', 'File Systems', 'Risk Management', 'Data Analysis Software', 'Virtual Environment', 'Artificial Neural Networks', 'Computer Vision', 'Computer Programming Tools', 'Probability', 'Statistical Hypothesis Testing', 'Database Systems', 'Plot (Graphics)', 'Data Mapping', 'Event-Driven Programming', 'Interactive Design', 'Peer Review', 'Test Automation', 'UI Components', 'Apache Hadoop', 'Apache Airflow', 'MySQL', 'Apache Kafka', 'Data Warehousing', 'Apache Spark', 'Data Store', 'IBM DB2', 'Collaborative Software', 'MongoDB', 'Grafana', 'OpenShift', 'Performance Tuning', 'Statistical Visualization', 'Graphing', 'Visualization (Computer Graphics)', 'Machine Learning Algorithms', 'Shiny (R Package)', 'Ggplot2', 'Animations', 'User Interface (UI)', 'Stress Management', 'Open Source Technology', 'Jest (JavaScript Testing Framework)', 'React.js', 'Mobile Development', 'Responsive Web Design', 'Javascript', 'Network Analysis', 'Penetration Testing', 'Authentications', 'Self Service Technologies', 'Cloud API', 'Predictive Analytics', 'Microservices', 'Service Oriented Architecture', 'API Gateway', 'Amazon DynamoDB', 'NoSQL', 'Serverless Computing', 'Amazon Web Services', 'Anomaly Detection', 'Numerical Analysis', 'MLOps (Machine Learning Operations)', 'Ideation', 'Expense Management', 'Document Management', 'Scalability', 'Content Creation', 'Microsoft Visual Studio', 'Infectious Diseases', 'Web Development Tools', 'Cloud Technologies', 'Cloud-Native Computing', 'Cloud Security', 'Node.JS', 'Embedded Systems', 'Linux', 'Internet Of Things', 'Functional Requirement', 'Electronic Hardware', 'System Design and Implementation', 'Hardware Design', 'Requirements Analysis', 'Embedded Software', 'Basic Electrical Systems', 'Calculus', 'PyTorch (Machine Learning Library)', 'Performance Metric', 'Performance Testing', 'Snowflake Schema', 'Site Reliability Engineering', 'Devops Tools', 'Databricks', 'R Programming', 'Other Programming Languages', 'Agile Software Development', 'Gherkin (Scripting Language)', 'Continuous Integration', 'Jenkins', 'Java Programming', 'Business Economics', 'Operational Analysis', 'Biostatistics', 'Data Management', 'Database Application', 'User Feedback', 'Data Quality', 'Stakeholder Engagement', 'Business Analysis', 'Target Audience', 'Marketing Strategies', 'A/B Testing', 'Business Metrics', 'Estimation', 'Return On Investment', 'Cloud Computing Architecture', 'Mathematical Software', 'Advanced Mathematics', 'Derivatives', 'Integral Calculus', 'Linux Administration', 'Encryption', 'Threat Modeling', 'Engineering Analysis', 'Vibrations', 'Mechanics', 'Finite Element Methods', 'Differential Equations', 'Distributed Computing', 'Scenario Testing', 'Hardware Architecture', 'Arithmetic', 'Logical Reasoning', 'Software Design Patterns', 'Systems Development', 'Software Development Methodologies', 'Design', '3D Modeling', 'Graphic and Visual Design', 'Functional Design', 'Descriptive Analytics', 'Database Development', 'Analysis', 'Biology', 'Molecular Biology', 'C++ (Programming Language)', 'Medical Imaging', 'Persona Development', 'Plan Execution', 'Information Architecture', 'Ajax', 'Life Sciences', 'Biochemistry', 'Markov Model', 'Medical Science and Research', 'Pharmacology', 'Radiology', 'Systems Architecture', 'Safety Assurance', 'Control Systems', 'Risk Management Framework', 'Microsoft Excel', 'Scala Programming', 'Neurology', 'Matlab', 'Technical Documentation', 'Application Performance Management', 'Network Troubleshooting', 'Incident Management', 'System Support', 'System Monitoring', 'Statistical Machine Learning', 'Accounting', 'Market Trend', 'Technical Analysis', 'Google Cloud Platform', 'Deductive Reasoning', 'Cyber Security Strategy', 'Software Visualization', 'Creative Design', 'Integration Testing', 'Mac OS', 'Cross Platform Development', 'Augmented Reality', 'Electronics', 'Digital Communications', 'Electrical Engineering', 'Engineering Calculations', 'Data Integrity', 'Rust (Programming Language)', 'Cloud Solutions', 'Analytics', 'Statistical Software', 'Sample Size Determination', 'Market Data', 'Finance', 'Equities', 'Risk Modeling', 'IBM Cognos Analytics', 'Containerization', 'DevOps', 'CI/CD', 'Application Frameworks', 'Web Servers', 'Model View Controller', 'Remote Access Systems', 'Go (Programming Language)', 'Angular', 'Torque (Physics)', 'Engineering', 'Simulation and Simulation Software', 'Infrastructure Architecture', 'Quantitative Research', 'Financial Forecasting', 'Securities Trading', 'Variance Analysis', 'Data Storage Technologies', 'Spatial Data Analysis', 'Computer Engineering', 'Computer Architecture', 'Application Specific Integrated Circuits', 'E-Commerce', 'Customer Service', 'User Flows', 'Semantic Web']

def normalize(text):
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', text.lower())).strip()

def get_skills(skill_strings, threshold=1):
    results = set()
    
    # Preprocess official skills
    normalized_skills = {normalize(skill): skill for skill in official_skills}
    skill_keys = list(normalized_skills.keys())
    
    for desc in skill_strings:
        desc_norm = normalize(desc)

        # Try partial token match first
        for key in skill_keys:
            if key in desc_norm:
                results.add(normalized_skills[key])
        
        # Fallback to fuzzy match if nothing found
        best_match = process.extractOne(
            desc_norm, skill_keys, scorer=fuzz.token_set_ratio
        )
        
        if best_match and best_match[1] >= threshold:
            results.add(normalized_skills[best_match[0]])
    
    return sorted(results)

def get_level(level_desc):
    return 'Beginner'

updated = []
courses = {}
with open("stepik_py.json", 'r', encoding='utf-8') as f:
    courses = json.load(f) 

for course in courses:
    if 'skills_learned' not in course.keys():
        continue
    if course['skills_learned'] is None:
        continue
    students = course['num_of_users']
    res = re.findall(r'[KM]', students)
    if len(res) == 0:
        students = int(students)
    elif res[0] == 'K':
        students = int(float(students.strip("K")) * 10e3)
    elif res[0] == 'M':
        students = int(float(students.strip("M")) * 10e6)

    rating = float(course['rating'].split('\n')[-1])
    price = course['price']
    if course['price'] in ['Бесплатно', 'Free']:
        price = 0
    else:
        price = int(price.split("₽")[0].replace(u"\xa0", ""))
    updated.append(
        {
            "url": course['course_url'],
            "title": course['title'],
            "author": course['author'],
            "students": students,
            "rating": rating,
            "difficulty": get_level(course['target_audience']),
            "skills": get_skills(course['skills_learned']) + ['Python'],
            "description": course['description'],
            "price": price,
            "source": "Stepik"
        }
    )
    print(updated[-1])

with open('stepik_clear.json', 'w', encoding='utf-8') as f:
    json.dump(updated, f, ensure_ascii=False)
