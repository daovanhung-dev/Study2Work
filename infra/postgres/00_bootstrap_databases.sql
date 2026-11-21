-- Study2Work V1-PILOT PostgreSQL bootstrap
-- Run with psql connected to a maintenance database such as postgres.
-- This file uses psql \gexec so CREATE DATABASE only runs when missing.

SELECT 'CREATE DATABASE identity_db'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'identity_db')
\gexec

SELECT 'CREATE DATABASE study_db'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'study_db')
\gexec

SELECT 'CREATE DATABASE work_db'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'work_db')
\gexec
