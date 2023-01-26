CREATE TABLE "user" (
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username VARCHAR(31) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(31),
    middle_name VARCHAR(31),
    last_name VARCHAR(31),
    access_level VARCHAR(31),
    create_time TIMESTAMP DEFAULT current_timestamp,
    last_login_time TIMESTAMP
);

CREATE TABLE redirect (
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    path VARCHAR(255) NOT NULL UNIQUE,
    target VARCHAR(1023),
    user Foreign Key (user) REFERENCES () -- TODO
    create_time TIMESTAMP DEFAULT current_timestamp,
    last_use_time TIMESTAMP,
    activate_time TIMESTAMP DEFAULT current_timestamp,
    expire_time TIMESTAMP,
    hit_count INT DEFAULT 0,
);

CREATE TABLE session (
    id int NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    token VARCHAR(1023) NOT NULL UNIQUE,
    user Foreign Key (user), -- TODO
    create_time TIMESTAMP DEFAULT current_timestamp,
    expire_time TIMESTAMP NOT NULL,
)
