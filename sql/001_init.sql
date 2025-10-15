

-- Create the schema for Bloom pipeline; Organizes all the bloom pipeline tables 
CREATE SCHEMA IF NOT EXISTS bloom;

-- Installs pgvector so we can work with embeddings (numerical representations of review text)
CREATE EXTENSION IF NOT EXISTS vector;

-- Necessary so we don't type "bloom." before each table
SET search_path TO bloom;


