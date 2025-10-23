CREATE SCHEMA IF NOT EXISTS bloom_core;

CREATE TABLE IF NOT EXISTS bloom_core.reviews_clean (
    id BIGSERIAL PRIMARY KEY,
    source_id BIGINT,
    clean_text TEXT NOT NULL,
    keywords TEXT[] DEFAULT ARRAY[]::TEXT[] NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_reviews_clean_source_id
    ON bloom_core.reviews_clean (source_id);

CREATE UNIQUE INDEX IF NOT EXISTS idx_reviews_clean_unique_text
    ON bloom_core.reviews_clean (clean_text);
