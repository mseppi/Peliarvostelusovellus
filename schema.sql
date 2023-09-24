DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS profile CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    pword TEXT
);

CREATE TABLE profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    username TEXT REFERENCES users(username),
    bio TEXT default 'placeholder'
);
