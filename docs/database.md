# Database Architecture

## Technology
Our primary database is PostgreSQL, chosen for its reliability and robust feature set. We use the SQLAlchemy ORM to interact with the database in Python.

## Schema
The main tables are `users`, `projects`, and `tasks`. The `users` table contains user credentials and profile information. All passwords are required to be hashed using bcrypt before being stored.

## Backups
Nightly backups are performed at 2:00 AM UTC. Backups are stored in a secure cloud storage bucket and are retained for 30 days.