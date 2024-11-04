CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT DEFAULT NULL,
    name TEXT DEFAULT NULL,
    email TEXT DEFAULT NULL,
    sms TEXT DEFAULT NULL,
    created TIMESTAMPTZ DEFAULT now(),
    lastseen TIMESTAMPTZ DEFAULT NULL
);

