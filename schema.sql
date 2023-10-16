DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS profile CASCADE;
DROP TABLE IF EXISTS games CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS comments CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    pword TEXT,
    admin_rights BOOLEAN default FALSE
);

CREATE TABLE profile (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    bio TEXT default '',
    fav_games TEXT default ''
);

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    title TEXT UNIQUE,
    release_year INTEGER,
    genre TEXT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    title TEXT,
    username TEXT,
    game_id INTEGER,
    review TEXT,
    rating INTEGER,
    likes INTEGER default 0,
    date_created TIMESTAMP default CURRENT_TIMESTAMP
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    username TEXT,
    review_id INTEGER,
    comment TEXT,
    likes INTEGER default 0,
    date_created TIMESTAMP default CURRENT_TIMESTAMP
);

INSERT INTO users (username, pword, admin_rights) VALUES ('admin', 'pbkdf2:sha256:600000$gxFzxmYkY6rCUedn$88417f36ff1bdac3d4b7e42905b4a54ba1af12c77249cf97b1375aae165f5a99', TRUE);
INSERT INTO profile (username, bio, fav_games) VALUES ('admin', 'I am the admin', 'admin');
