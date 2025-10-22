

CREATE TABLE IF NOT EXISTS bloom_analytics.actions (
    id SERIAL PRIMARY KEY,
    cluster_id INT NOT NULL REFERENCES bloom_analytics.clusters(id), --connects a cluster to an action
    pain_point TEXT NOT NULL,
    recommended_action TEXT,
    impact_score FLOAT DEFAULT 0.0,
    effort_score FLOAT DEFAULT 0.0, --how difficult it is to implement the action
    priority_rank INT,
    supporting_quotes TEXT[], --array of quotes supporting the pain point
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
