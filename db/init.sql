-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- User accounts
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    login VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    creation_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User profile information
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    background TEXT,
    background_vector VECTOR(256),
    goals TEXT,
    goals_vector VECTOR(256),
    goal_vacancy VARCHAR(100),
    goal_vacancy_vector VECTOR(256)
);

-- User skills
CREATE TABLE user_skills (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    skill VARCHAR(100) NOT NULL,
    skill_vector VECTOR(256),
    skill_level VARCHAR(20) CHECK (skill_level IN ('Beginner', 'Intermediate', 'Advanced')),
    level_vector VECTOR(64),
    PRIMARY KEY (user_id, skill)
);

-- User goals
CREATE TABLE user_goals (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    goal VARCHAR(100) NOT NULL,
    goal_vector VECTOR(256),
    PRIMARY KEY (user_id, goal)
);

-- Learning resources
CREATE TABLE resource (
    resource_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_type VARCHAR(20) CHECK (resource_type IN ('Course', 'Article')),
    title VARCHAR(100) NOT NULL,
    summary TEXT,
    summary_vector VECTOR(256),
    content TEXT NOT NULL,
    level VARCHAR(20) CHECK (level IN ('Beginner', 'Intermediate', 'Advanced', 'All Levels')),
    price DECIMAL(10,2),
    language VARCHAR(50) DEFAULT 'English',
    duration_hours INTEGER,
    platform VARCHAR(50),
    rating DECIMAL(3,1) CHECK (rating BETWEEN 0 AND 5),
    published_date DATE,
    certificate_available BOOLEAN DEFAULT FALSE,
    skills_covered VARCHAR(100)[],
    skills_covered_vector VECTOR(256)[]
);

CREATE TABLE user_roadmap (
    roadmap_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE roadmap_node (
    node_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    roadmap_id UUID REFERENCES User_Roadmap(roadmap_id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    summary TEXT,
    resource_id UUID,
    progress INTEGER CHECK (progress BETWEEN 0 AND 100) DEFAULT 0
);

CREATE TABLE roadmap_link (
    link_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    roadmap_id UUID REFERENCES User_Roadmap(roadmap_id) ON DELETE CASCADE,
    from_node UUID REFERENCES Roadmap_Node(node_id) ON DELETE CASCADE,
    to_node UUID REFERENCES Roadmap_Node(node_id) ON DELETE CASCADE
);

-- Insert users
INSERT INTO users (login, password) VALUES
('react_expert', 'hashed_password_1'),
('career_switcher_2024', 'hashed_password_2'),
('python_data_wizard', 'hashed_password_3'),
('cloud_nomad', 'hashed_password_4'),
('design_to_code', 'hashed_password_5');

-- Insert profiles
INSERT INTO user_profiles (id, background, goals, goal_vacancy) VALUES
(
    (SELECT id FROM users WHERE login = 'react_expert'),
    '5+ years building responsive UIs for Fortune 500 companies',
    'Lead full-stack projects within 9 months',
    'Senior Full-Stack Developer'
),
(
    (SELECT id FROM users WHERE login = 'career_switcher_2024'),
    'Former teacher completed 6-month coding bootcamp',
    'Land entry-level developer role in 6 months',
    'Junior Software Engineer'
),
(
    (SELECT id FROM users WHERE login = 'python_data_wizard'),
    '2 years analyzing business data for e-commerce',
    'Transition to ML team within current company',
    'Machine Learning Engineer'
),
(
    (SELECT id FROM users WHERE login = 'cloud_nomad'),
    '3 years managing AWS infrastructure for startups',
    'Earn AWS Solutions Architect Professional cert',
    'Cloud Architect'
),
(
    (SELECT id FROM users WHERE login = 'design_to_code'),
    '4 years creating interfaces for mobile apps',
    'Build interactive prototypes without engineers',
    'UI Engineer'
);

-- Insert skills for react_expert
INSERT INTO user_skills (user_id, skill, skill_level) VALUES
(
    (SELECT id FROM users WHERE login = 'react_expert'),
    'React',
    'Advanced'
),
(
    (SELECT id FROM users WHERE login = 'react_expert'),
    'TypeScript',
    'Advanced'
),
(
    (SELECT id FROM users WHERE login = 'react_expert'),
    'Redux',
    'Intermediate'
),
(
    (SELECT id FROM users WHERE login = 'react_expert'),
    'Jest',
    'Intermediate'
);

-- Insert skills for career_switcher_2024
INSERT INTO user_skills (user_id, skill, skill_level) VALUES
(
    (SELECT id FROM users WHERE login = 'career_switcher_2024'),
    'JavaScript',
    'Intermediate'
),
(
    (SELECT id FROM users WHERE login = 'career_switcher_2024'),
    'HTML/CSS',
    'Intermediate'
),
(
    (SELECT id FROM users WHERE login = 'career_switcher_2024'),
    'Express.js',
    'Beginner'
);

-- Insert skills for python_data_wizard
INSERT INTO user_skills (user_id, skill, skill_level) VALUES
(
    (SELECT id FROM users WHERE login = 'python_data_wizard'),
    'Python',
    'Advanced'
),
(
    (SELECT id FROM users WHERE login = 'python_data_wizard'),
    'Pandas',
    'Advanced'
),
(
    (SELECT id FROM users WHERE login = 'python_data_wizard'),
    'SQL',
    'Intermediate'
),
(
    (SELECT id FROM users WHERE login = 'python_data_wizard'),
    'Tableau',
    'Intermediate'
);

-- Insert skills for cloud_nomad
INSERT INTO user_skills (user_id, skill, skill_level) VALUES
(
    (SELECT id FROM users WHERE login = 'cloud_nomad'),
    'Terraform',
    'Intermediate'
),
(
    (SELECT id FROM users WHERE login = 'cloud_nomad'),
    'Docker',
    'Advanced'
),
(
    (SELECT id FROM users WHERE login = 'cloud_nomad'),
    'CI/CD Pipelines',
    'Intermediate'
);

-- Insert skills for design_to_code
INSERT INTO user_skills (user_id, skill, skill_level) VALUES
(
    (SELECT id FROM users WHERE login = 'design_to_code'),
    'Figma',
    'Advanced'
),
(
    (SELECT id FROM users WHERE login = 'design_to_code'),
    'UI Prototyping',
    'Advanced'
),
(
    (SELECT id FROM users WHERE login = 'design_to_code'),
    'Design Systems',
    'Intermediate'
);

-- Insert goals for react_expert
INSERT INTO user_goals (user_id, goal) VALUES
(
    (SELECT id FROM users WHERE login = 'react_expert'),
    'Node.js'
),
(
    (SELECT id FROM users WHERE login = 'react_expert'),
    'GraphQL'
),
(
    (SELECT id FROM users WHERE login = 'react_expert'),
    'AWS'
);

-- Insert goals for career_switcher_2024
INSERT INTO user_goals (user_id, goal) VALUES
(
    (SELECT id FROM users WHERE login = 'career_switcher_2024'),
    'React'
),
(
    (SELECT id FROM users WHERE login = 'career_switcher_2024'),
    'MongoDB'
),
(
    (SELECT id FROM users WHERE login = 'career_switcher_2024'),
    'System Design'
);

-- Insert goals for python_data_wizard
INSERT INTO user_goals (user_id, goal) VALUES
(
    (SELECT id FROM users WHERE login = 'python_data_wizard'),
    'Scikit-learn'
),
(
    (SELECT id FROM users WHERE login = 'python_data_wizard'),
    'TensorFlow'
),
(
    (SELECT id FROM users WHERE login = 'python_data_wizard'),
    'MLOps'
);

-- Insert goals for cloud_nomad
INSERT INTO user_goals (user_id, goal) VALUES
(
    (SELECT id FROM users WHERE login = 'cloud_nomad'),
    'Kubernetes'
),
(
    (SELECT id FROM users WHERE login = 'cloud_nomad'),
    'Serverless Architecture'
),
(
    (SELECT id FROM users WHERE login = 'cloud_nomad'),
    'GCP'
);

-- Insert goals for design_to_code
INSERT INTO user_goals (user_id, goal) VALUES
(
    (SELECT id FROM users WHERE login = 'design_to_code'),
    'React'
),
(
    (SELECT id FROM users WHERE login = 'design_to_code'),
    'CSS Animations'
),
(
    (SELECT id FROM users WHERE login = 'design_to_code'),
    'Design-Dev Handoff'
);
