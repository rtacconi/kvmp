-- migrate:up
SET time zone 'UTC';

CREATE TABLE xml_templates (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(50)  NOT NULL,   
    user_id INTEGER REFERENCES users(id) NOT NULL,
    vm_info_id INTEGER REFERENCES users(id) NOT NULL,
    xml_data text[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- migrate:down
DROP TABLE xml_templates;
