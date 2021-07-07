/*
    - info: This SQL code generates simple SQLite3 db schema for MControl_server database
    - source: https://editor.ponyorm.com/user/vickhov/MControl_database/sqlite
*/

/*
    - [warn]: outdated db version!
*/

CREATE TABLE "User" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "username" TEXT UNIQUE NOT NULL,
  "password" TEXT NOT NULL,
  "role" TEXT NOT NULL
);

CREATE TABLE "Script" (
  "script_id" INTEGER NOT NULL PRIMARY KEY,
  "created_by" INTEGER NOT NULL REFERENCES "User" ("id") ON DELETE CASCADE,
  "script_name" TEXT UNIQUE NOT NULL,
  "description" TEXT NOT NULL,
  "content" JSON NOT NULL,
  "editor_data" JSON NOT NULL,
  "created" DATETIME NOT NULL,
  "updated" DATETIME
);

CREATE INDEX "idx_script__created_by" ON "Script" ("created_by")