DROP TABLE IF EXISTS forums CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS votes CASCADE;
DROP TABLE IF EXISTS threads CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS forum_for_users CASCADE;

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
  user_id  INTEGER REFERENCES users(user_id) ON DELETE CASCADE,           -- ID пользователя, создавшего форум
  posts    INTEGER DEFAULT 0,                                             -- Количество постов в форуме
  slug     CITEXT UNIQUE NOT NULL,                                        -- Человекопонятный URL (уникальное поле)
  threads  INTEGER DEFAULT 0,                                             -- Количество тредов в форуме
  title    TEXT,                                                          -- Название форума
  "user"   CITEXT                                                         -- Имя пользователя, создавшего форум
);

CREATE TABLE IF NOT EXISTS forum_for_users (
  forum_id INTEGER REFERENCES forums (forum_id) ON DELETE CASCADE NOT NULL,
  user_id  INTEGER REFERENCES users (user_id) ON DELETE CASCADE NOT NULL,
  nickname CITEXT COLLATE "ucs_basic",                                    -- Уникальный nick пользователя
  about    TEXT,                                                          -- Описание пользователя
  email    CITEXT,                                                        -- email пользователя
  fullname TEXT                                                           -- полное имя пользователя
);

ALTER TABLE forum_for_users
    ADD CONSTRAINT forum_for_users_cstr
    UNIQUE(forum_id, user_id);

CREATE TABLE threads (
  id serial CONSTRAINT firstkey_th PRIMARY KEY,                           -- ID ветки обсуждения
  forum_id  INTEGER REFERENCES forums(forum_id) ON DELETE CASCADE,        -- ID форума, к которому относится тред
  user_id   INTEGER REFERENCES users(user_id) ON DELETE CASCADE,          -- ID пользователя, создавшего ветку обсуждения
  author    CITEXT,                                                       -- Имя пользователя, создавшего форум
  created   TIMESTAMP WITH TIME ZONE DEFAULT now(),                       -- Дата создания ветки описания
  forum     CITEXT,                                                       -- Человекопонятный URL для идентификации форума
  message   TEXT,                                                         -- Описание ветки обсуждения
  slug      CITEXT DEFAULT NULL,                                          -- Человекопонятный URL
  title     TEXT NOT NULL,                                                -- Заголовок ветки обсуждения
  votes     SMALLINT DEFAULT 0
);

CREATE TABLE posts (
  id        serial CONSTRAINT firstkey_p PRIMARY KEY,                      -- ID поста
  user_id   INTEGER REFERENCES users(user_id) ON DELETE CASCADE,           -- ID пользователя, создавшего пост
  thread    INTEGER REFERENCES threads(id) ON DELETE CASCADE,              -- ID ветки обсуждения в котором находится сообщение
  forum_id  INTEGER REFERENCES forums(forum_id) ON DELETE CASCADE,         -- ID форума в котором находится сообщение
  author    CITEXT,                                                        -- Имя автора поста
  created   TIMESTAMP WITH TIME ZONE DEFAULT now(),                        -- Дата создания поста
  forum     CITEXT,                                                        -- Идентификатор форума
  isEdited  BOOLEAN DEFAULT FALSE,                                         -- Было ли изменино сообщение
  message   TEXT,                                                          -- Сообщение поста
  parent    INTEGER DEFAULT 0,                                             -- Идентификатор родительского сообщения
  path      INTEGER []                                                     -- Путь до подительского поста

);

CREATE TABLE votes (
  vote_id   serial CONSTRAINT firstkey_v PRIMARY KEY,                     -- ID голоса
  user_id   INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE, -- ID проголосовавшего юзера
  thread_id INTEGER NOT NULL REFERENCES threads(id) ON DELETE CASCADE,    -- ID треда, в котором проголосовали
  voice     SMALLINT                                                      -- Значение голоса (принимает значение -1 или 1)
);

ALTER TABLE votes
    ADD CONSTRAINT vote_user_thread
    UNIQUE(user_id, thread_id);


--==================================== TRIGGERS ====================================

CREATE OR REPLACE FUNCTION update_thread_votes()
  RETURNS TRIGGER AS $$
BEGIN
  IF (TG_OP = 'UPDATE')
      THEN
        IF NEW.voice != OLD.voice
            THEN UPDATE threads
                 SET votes = votes + (2 * NEW.voice)
                 WHERE threads.id = NEW.thread_id;
                 RETURN NEW;
        ELSE
            RETURN NEW;
        END IF;

  ELSE

    UPDATE threads
    SET votes = votes + NEW.voice
    WHERE threads.id = NEW.thread_id;
    RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_thread_votes
  AFTER INSERT OR UPDATE
  ON votes
  FOR EACH ROW
EXECUTE PROCEDURE update_thread_votes();

CREATE OR REPLACE FUNCTION insert_forum_for_user()
  RETURNS TRIGGER AS $$
BEGIN

  LOCK TABLE forum_for_users;

  INSERT INTO forum_for_users (forum_id, user_id, nickname, email, about, fullname)
  (
    SELECT  NEW.forum_id, NEW.user_id, u.nickname, u.email, u.about, u.fullname
    FROM users u
    WHERE u.user_id = new.user_id
    FOR NO KEY UPDATE
  )
  ON CONFLICT DO NOTHING;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION insert_post_for_user()
  RETURNS TRIGGER AS $$
BEGIN

  LOCK TABLE forum_for_users;

  INSERT INTO forum_for_users (forum_id, user_id, nickname, email, about, fullname)
  (
    SELECT  NEW.forum_id, NEW.user_id, u.nickname, u.email, u.about, u.fullname
    FROM users u
    WHERE u.user_id = new.user_id
    FOR NO KEY UPDATE
  )
  ON CONFLICT DO NOTHING;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER insert_user_for_post_tg
  AFTER INSERT
  ON posts
  FOR EACH ROW
EXECUTE PROCEDURE insert_post_for_user();

CREATE TRIGGER insert_user_for_thread_tg
  AFTER INSERT
  ON threads
  FOR EACH ROW
EXECUTE PROCEDURE insert_forum_for_user();

--==================================== INDEXES ====================================
--
-- --=========== FORUMS ===========
--
CREATE INDEX forums_slug_all_idx
  ON forums (slug, user, title, threads, posts, forum_id);

CREATE INDEX forums_slug_uid_idx
  ON forums (slug, forum_id);

CREATE INDEX forums_users_index
  ON forums (user_id);

CREATE INDEX forums_slug_index
  ON forums (slug);
-- 
-- --=========== POSTS ===========
--
CREATE INDEX IF NOT EXISTS posts_thread_path_index
  ON posts (thread, path);

CREATE INDEX IF NOT EXISTS posts_id_thread_index
  ON posts (id, thread);

CREATE INDEX IF NOT EXISTS posts_thread_id_index
  ON posts (thread, id);

CREATE INDEX posts_thread_parent_path_uid_index
  ON posts (thread, parent, path, id);

CREATE INDEX posts_uid_thread_parent_index
  ON posts (id, thread, parent);

CREATE index posts_uid_path_index
  ON posts (id, path);

CREATE INDEX posts_threads_index
  ON posts (thread);

CREATE INDEX posts_forums_index
  ON posts (forum_id);

CREATE INDEX posts_parent_index
  ON posts (parent);

CREATE INDEX posts_users_index
  ON posts (user_id);
--
-- --=========== THREADS ===========
-- 
create index threads_forum_id_created_index
  on threads (forum_id, created);

CREATE INDEX threads_forums_index
  ON threads (forum_id);

CREATE INDEX threads_users_index
  ON threads (user_id);

CREATE INDEX threads_slug_index
  ON threads (slug);
--
-- --=========== USERS ===========
--
CREATE INDEX users_nickname_collate_email_about_fullname_uid_index
  ON users (nickname, about, email, fullname, user_id);

CREATE INDEX users_nickname_index
  ON users (nickname);

CREATE INDEX users_email_index
  ON users (email);
-- 
-- --=========== FORUM_FOR_USER ===========
-- 
CREATE INDEX users_for_forum_full_index
  on forum_for_users (forum_id, user_id, nickname COLLATE "ucs_basic", email, about, fullname);
-- 
-- --=========== VOTES ===========
--
CREATE INDEX vote_threads_index
  ON votes (thread_id);

CREATE INDEX vote_users_index
  ON votes (user_id);

