-- migrate:up
SET time zone 'UTC';
CREATE TABLE servers (
    id SERIAL PRIMARY KEY,
    host VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    key_file VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- migrate:down
DROP TABLE servers