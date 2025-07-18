-- User accounts
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    login VARCHAR(50) UNIQUE NOT NULL,
    mail VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    creation_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    background TEXT,
    education TEXT,
    goals TEXT,
    goal_vacancy VARCHAR(100),
    is_active BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE
);
-- User skills
CREATE TABLE user_skills (
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    skill VARCHAR(100) NOT NULL,
    skill_level VARCHAR(20) CHECK (
        skill_level IN ('Beginner', 'Intermediate', 'Advanced')
    ),
    is_goal BOOLEAN,
    PRIMARY KEY (user_id, skill)
);
-- Learning resources
CREATE TABLE resource (
    resource_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resource_type VARCHAR(20) CHECK (resource_type IN ('Course', 'Article')),
    title VARCHAR(100) NOT NULL,
    summary TEXT,
    content TEXT NOT NULL,
    level VARCHAR(20) CHECK (
        level IN (
            'Beginner',
            'Intermediate',
            'Advanced',
            'All Levels'
        )
    ),
    price DECIMAL(10, 2),
    language VARCHAR(50) DEFAULT 'English',
    duration_hours INTEGER,
    platform VARCHAR(50),
    rating DECIMAL(3, 1) CHECK (
        rating BETWEEN 0 AND 5
    ),
    published_date DATE,
    certificate_available BOOLEAN DEFAULT FALSE,
    skills_covered VARCHAR(100) []
);
CREATE TABLE user_roadmap (
    roadmap_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE
);
CREATE TABLE roadmap_node (
    node_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    roadmap_id UUID REFERENCES User_Roadmap(roadmap_id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    summary TEXT,
    resource_id UUID,
    progress VARCHAR(50) DEFAULT 'Not started'
);
CREATE TABLE roadmap_link (
    link_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    roadmap_id UUID REFERENCES User_Roadmap(roadmap_id) ON DELETE CASCADE,
    from_node UUID REFERENCES Roadmap_Node(node_id) ON DELETE CASCADE,
    to_node UUID REFERENCES Roadmap_Node(node_id) ON DELETE CASCADE
);
CREATE TABLE roadmap_history (
    roadmap_id UUID REFERENCES User_Roadmap(roadmap_id) ON DELETE CASCADE,
    title TEXT,
    node_id UUID REFERENCES Roadmap_Node(node_id) ON DELETE CASCADE,
    last_opened TIMESTAMP WITH TIME ZONE,
    progress VARCHAR(50)
);
CREATE TABLE roadmap_feedback (
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    node_id UUID REFERENCES Roadmap_Node(node_id) ON DELETE CASCADE,
    reason VARCHAR(50)
);