CREATE TABLE IF NOT EXISTS Users(
    id BIGINT PRIMARY KEY,
    username VARCHAR(30),
    first_name TEXT,
    last_name TEXT,
    balance INT DEFAULT 0,
    referral BIGINT REFERENCES Users(id),
    registed timestamptz DEFAULT now(),
    confirm BOOLEAN DEFAULT false
);

