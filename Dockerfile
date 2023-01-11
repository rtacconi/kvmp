FROM postgres:latest

# Create a data volume
VOLUME /var/lib/postgresql/data

# Expose the PostgreSQL port
EXPOSE 5432
