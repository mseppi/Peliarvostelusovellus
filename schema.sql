DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS profile CASCADE;



CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    pword TEXT,
    system_role TEXT
);

CREATE TABLE profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    username TEXT REFERENCES users(username),
    bio TEXT default 'placeholder'
);

INSERT INTO users (username, pword, system_role) VALUES ('admin', 'admin', 'admin');