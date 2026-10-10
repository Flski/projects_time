PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    login TEXT NOT NULL UNIQUE CHECK(LENGTH(login) BETWEEN 4 AND 100),
    password_hash TEXT NOT NULL CHECK(LENGTH(password_hash) BETWEEN 8 AND 10000)
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL CHECK(LENGTH(name) BETWEEN 1 AND 100),
    description TEXT CHECK(LENGTH(description) BETWEEN 1 AND 10000),
    status TEXT NOT NULL CHECK(status in ('active', 'completed')),
    created_at TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES clients (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL CHECK(LENGTH(name) BETWEEN 1 AND 100),
    description TEXT CHECK(LENGTH(description) BETWEEN 1 AND 10000),
    status TEXT NOT NULL CHECK(status in ('start', 'pause', 'stop')),
    created_at TEXT NOT NULL,
    project_id INTEGER NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS time_logs (
    id INTEGER PRIMARY KEY,
    datetime_start TEXT NOT NULL,
    datetime_end TEXT,
    comment TEXT CHECK(LENGTH(comment) BETWEEN 1 AND 1000),
    duration TEXT,
    task_id INTEGER NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
);

CREATE INDEX index_user_id ON projects(user_id);
CREATE INDEX index_project_id ON tasks(project_id);
CREATE INDEX index_task_id ON time_logs(task_id);
CREATE UNIQUE INDEX index_login ON clients(login);