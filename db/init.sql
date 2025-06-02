-- db/init.sql

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO users (name, email) VALUES
    ('Alice Example', 'alice@example.com'),
    ('Bob Example', 'bob@example.com');
