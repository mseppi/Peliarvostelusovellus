CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    role TEXT DEFAULT 'user'
);

CREATE TABLE profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user(id),
    name TEXT REFERENCES user(name),
    bio TEXT default 'placeholder',
);

INSERT INTO user (name, password, role) VALUES ('admin', 'admin', 'admin');