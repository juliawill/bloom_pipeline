
--Hello world

CREATE TABLE IF NOT EXISTS bloom_raw.reviews (
    id SERIAL PRIMARY KEY,
    source TEXT,            -- Sephora, Ulta, TikTok
    url TEXT,               -- Link to the page
    review_text TEXT,       -- Raw text scraped from the site
    rating FLOAT,           -- If available
    date TIMESTAMP,         -- Date the review was posted
    created_at TIMESTAMP DEFAULT NOW()  -- When it was inserted
);
