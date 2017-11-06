DROP TABLE IF EXISTS forums CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS votes CASCADE;
DROP TABLE IF EXISTS threads CASCADE;
DROP TABLE IF EXISTS posts CASCADE;

CREATE TABLE users (
  user_id  serial CONSTRAINT firstkey_u PRIMARY KEY,                      -- ID форума
  nickname CITEXT COLLATE "ucs_basic" UNIQUE NOT NULL,                    -- Уникальный nick пользователя
  about    TEXT,                                                          -- Описание пользователя
  email    CITEXT,                                                        -- email пользователя
  fullname TEXT,                                                          -- полное имя пользователя
  CONSTRAINT uniq_email UNIQUE (email)                                    -- ограничение на email, как уникальное поле
);

CREATE TABLE forums (
  forum_id serial CONSTRAINT firstkey_f PRIMARY KEY,                      -- ID форума
  user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,            -- ID пользователя, создавшего форум
  posts INTEGER DEFAULT 0,                                                -- Количество постов в форуме
  slug CITEXT UNIQUE NOT NULL,                                            -- Человекопонятный URL (уникальное поле)
  threads INTEGER DEFAULT 0,                                              -- Количество тредов в форуме
  title TEXT,                                                             -- Название форума
  "user" CITEXT                                                           -- Имя пользователя, создавшего форум
);

CREATE TABLE threads (
  id serial CONSTRAINT firstkey_th PRIMARY KEY,                    -- ID ветки обсуждения
  forum_id  INTEGER REFERENCES forums(forum_id) ON DELETE CASCADE,        -- ID форума, к которому относится тред
  user_id   INTEGER REFERENCES users(user_id) ON DELETE CASCADE,          -- ID пользователя, создавшего ветку обсуждения
  author    CITEXT,                                                       -- Имя пользователя, создавшего форум
  created   TIMESTAMP WITH TIME ZONE DEFAULT now(),                                     -- Дата создания ветки описания
  forum     CITEXT,                                                       -- Человекопонятный URL для идентификации форума
  message   TEXT,                                                         -- Описание ветки обсуждения
  slug      CITEXT DEFAULT NULL,                                                -- Человекопонятный URL
  title     TEXT NOT NULL,                                                -- Заголовок ветки обсуждения
  votes     SMALLINT DEFAULT 0
);

CREATE TABLE posts (
  post_id serial CONSTRAINT firstkey_p PRIMARY KEY,                       -- ID поста
  user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,            -- ID пользователя, создавшего пост
  thread_id INTEGER REFERENCES threads(id) ON DELETE CASCADE,      -- ID ветки обсуждения в котором находится сообщение
  forum_id INTEGER REFERENCES forums(forum_id) ON DELETE CASCADE,         -- ID форума в котором находится сообщение
  created TIMESTAMP WITH TIME ZONE DEFAULT now(),                                       -- Дата создания поста
  isEdited BOOLEAN DEFAULT FALSE,                                         -- Было ли изменино сообщение
  message TEXT,                                                           -- Сообщение поста
  parent_id INTEGER DEFAULT 0,                                            -- Идентификатор родительского сообщения
  path     INTEGER []                                                     -- Путь до подительского поста

);

CREATE TABLE votes (
  vote_id   serial CONSTRAINT firstkey_v PRIMARY KEY,                     -- ID голоса
  user_id   INTEGER REFERENCES users(user_id) ON DELETE CASCADE,          -- ID проголосовавшего юзера
  thread_id INTEGER REFERENCES threads(id) ON DELETE CASCADE,      -- ID треда, в котором проголосовали
  voice     SMALLINT                                                      -- Значение голоса (принимает значение -1 или 1)
);