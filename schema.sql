DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS profile CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    pword TEXT
);

CREATE TABLE profile (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    bio TEXT default 'placeholder',
    fav_games TEXT default 'placeholder'
);
