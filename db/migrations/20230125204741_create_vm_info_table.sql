-- migrate:up
SET time zone 'UTC';

CREATE TABLE vm_infos (
    id SERIAL PRIMARY KEY,
    data JSON NOT NULL,
    user_id INTEGER REFERENCES users(id),
    server_id INTEGER REFERENCES servers(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- migrate:down
DROP TABLE vm_infos;