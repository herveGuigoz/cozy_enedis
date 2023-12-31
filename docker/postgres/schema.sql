CREATE TABLE IF NOT EXISTS clients (
  id TEXT PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  issuer TEXT NOT NULL,
  secret TEXT NOT NULL,
  registration_access_token TEXT NOT NULL,
  access_token TEXT DEFAULT NULL,
  refresh_token TEXT DEFAULT NULL,
  created_at TIMESTAMP with TIME ZONE NOT NULL DEFAULT timezone('utc' :: text, now())
);

CREATE UNIQUE INDEX client_issuer ON clients(issuer);