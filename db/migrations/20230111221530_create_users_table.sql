-- migrate:up
SET time zone 'UTC';
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
INSERT INTO users (username, email, password, is_admin, created_at) VALUES ('admin', 'admin@gmail.com', md5('password'), 't', '2022-01-01 12:00:00.000000-07'::timestamptz);

-- migrate:down
drop table users;
