FROM pgvector/pgvector:pg16

# Copy all SQL schema files into the standard Postgres init directory so they run on first boot.
COPY sql/ /docker-entrypoint-initdb.d/
