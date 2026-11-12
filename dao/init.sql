CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL CHECK(LENGTH(login)>=4 AND LENGTH(login)<=100),
    password_hash TEXT NOT NULL CHECK(LENGTH(password_hash)>=16 AND LENGTH(password_hash)<=10000),
    UNIQUE(login)
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK(LENGTH(name)>=1 AND LENGTH(name)<=100),
    description TEXT CHECK(LENGTH(description)<=10000),
    created_at TEXT NOT NULL CHECK(LENGTH(created_at)>=1 AND LENGTH(created_at)<=1000),
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES clients (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK(LENGTH(name)>=1 AND LENGTH(name)<=100),
    description TEXT CHECK(LENGTH(description)<=10000),
    status TEXT NOT NULL CHECK(status in ('passive', 'start', 'pause', 'stop')),
    created_at TEXT NOT NULL CHECK(LENGTH(created_at)>=1 AND LENGTH(created_at)<=1000),
    project_id INTEGER NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS time_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime_start TEXT NOT NULL CHECK(LENGTH(datetime_start)>=1 AND LENGTH(datetime_start)<=1000),
    datetime_end TEXT CHECK(LENGTH(datetime_end)>=1 AND LENGTH(datetime_end)<=1000),
    duration TEXT CHECK(LENGTH(duration)>=1 AND LENGTH(duration)<=1000),
    task_id INTEGER NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS index_login ON clients(login);
CREATE INDEX IF NOT EXISTS index_project_id ON projects(id);
CREATE INDEX IF NOT EXISTS index_task_id ON tasks(id);
