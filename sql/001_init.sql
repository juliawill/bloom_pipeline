

-- Creates the schema for Bloom pipeline; Organizes all the bloom pipeline tables 
CREATE SCHEMA IF NOT EXISTS bloom;

-- Creates sub-schemas for organization
CREATE SCHEMA IF NOT EXISTS bloom_raw;
CREATE SCHEMA IF NOT EXISTS bloom_core;
CREATE SCHEMA IF NOT EXISTS bloom_analytics;


-- Installs pgvector so we can work with embeddings (numerical representations of review text)
CREATE EXTENSION IF NOT EXISTS vector;

-- Necessary so we don't type "bloom." before each table
SET search_path TO bloom;


