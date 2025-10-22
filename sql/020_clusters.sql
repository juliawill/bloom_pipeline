--10/16/25
-- 020_clusters.sql


CREATE TABLE IF NOT EXISTS bloom_analytics.clusters (
    id SERIAL PRIMARY KEY,
    cluster_label TEXT NOT NULL, --Name for the cluster
    num_reviews INT NOT NULL DEFAULT 0, --Counts how many reivews are in a cluster
    avg_sentiment FLOAT DEFAULT 0.0, --Score for how good/bad the review is
    severity_score FLOAT DEFAULT 0.0, --Extra metric for cluster importance (size × negative sentiment maybe)
    created_at TIMESTAMP DEFAULT NOW(), --When cluster created
    updated_at TIMESTAMP DEFAULT NOW() --When cluster updated

);