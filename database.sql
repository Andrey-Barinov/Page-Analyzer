DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    id serial PRIMARY KEY,
    name varchar(255) UNIQUE NOT NULL,
    created_at date DEFAULT CURRENT_DATE
);
