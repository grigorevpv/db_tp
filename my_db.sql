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
  user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,            -- ID пользователя, создавшего форум
  posts INTEGER DEFAULT 0,                                                -- Количество постов в форуме
  slug CITEXT UNIQUE NOT NULL,                                            -- Человекопонятный URL (уникальное поле)
  threads INTEGER DEFAULT 0,                                              -- Количество тредов в форуме
  title TEXT,                                                             -- Название форума
  "user" CITEXT                                                           -- Имя пользователя, создавшего форум
);

CREATE TABLE IF NOT EXISTS forum_for_users (
  forum_id INTEGER REFERENCES forums (forum_id) ON DELETE CASCADE NOT NULL,
  user_id  INTEGER REFERENCES users (user_id) ON DELETE CASCADE NOT NULL,
  nickname CITEXT COLLATE "ucs_basic" UNIQUE NOT NULL,                    -- Уникальный nick пользователя
  about    TEXT,                                                          -- Описание пользователя
  email    CITEXT,                                                        -- email пользователя
  fullname TEXT                                                           -- полное имя пользователя
);

ALTER TABLE forum_for_users
    ADD CONSTRAINT forum_for_users_cstr
    UNIQUE(forum_id, user_id);

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
  id serial CONSTRAINT firstkey_p PRIMARY KEY,                       -- ID поста
  user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,            -- ID пользователя, создавшего пост
  thread INTEGER REFERENCES threads(id) ON DELETE CASCADE,             -- ID ветки обсуждения в котором находится сообщение
  forum_id INTEGER REFERENCES forums(forum_id) ON DELETE CASCADE,         -- ID форума в котором находится сообщение
  author CITEXT,                                                          -- Имя автора поста
  created TIMESTAMP WITH TIME ZONE DEFAULT now(),                         -- Дата создания поста
  forum CITEXT,                                                           -- Идентификатор форума
  isEdited BOOLEAN DEFAULT FALSE,                                         -- Было ли изменино сообщение
  message TEXT,                                                           -- Сообщение поста
  parent INTEGER DEFAULT 0,                                            -- Идентификатор родительского сообщения
  path     INTEGER []                                                     -- Путь до подительского поста

);

CREATE TABLE votes (
  vote_id   serial CONSTRAINT firstkey_v PRIMARY KEY,                     -- ID голоса
  user_id   INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,          -- ID проголосовавшего юзера
  thread_id INTEGER NOT NULL REFERENCES threads(id) ON DELETE CASCADE,             -- ID треда, в котором проголосовали
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

CREATE OR REPLACE FUNCTION inser_forum_for_user()
  RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO forum_for_users (forum_id, user_id, nickname, email, about, fullname)
  (
    SELECT  NEW.forum_id, NEW.user_id, u.nickname, u.email, u.about, u.fullname
    FROM users u
    WHERE u.user_id = new.user_id
  )
  ON CONFLICT DO NOTHING;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER inser_user_for_post
  AFTER INSERT
  ON posts
  FOR EACH ROW
EXECUTE PROCEDURE inser_forum_for_user();

CREATE TRIGGER inser_user_for_thread
  AFTER INSERT
  ON threads
  FOR EACH ROW
EXECUTE PROCEDURE inser_forum_for_user();

--==================================== INDEXES ====================================

-- --=========== FORUMS ===========
-- 
CREATE INDEX forums_slug_idx
  ON forums (slug);

CREATE INDEX forums_users_idx
  ON forums (user_id);
-- 
CREATE INDEX forums_slug_uid_idx
  ON forums (slug, forum_id);
-- 
-- CREATE INDEX forums_slug_all_idx
--   ON forums (slug, user, title, threads, posts, forum_id);
-- 
-- --=========== POSTS ===========
-- 
-- CREATE INDEX posts_threads_idx
--   ON posts (thread);
-- 
-- CREATE INDEX posts_forums_idx
--   ON posts (forum_id);
-- 
-- CREATE INDEX posts_users_idx
--   ON posts (user_id);
-- 
-- CREATE INDEX posts_parent_idx
--   ON posts (parent);
-- 
-- ------------------------------------------------------------------------------------------------------------------------
-- CREATE INDEX IF NOT EXISTS posts_uid_thread_idx
--   ON posts (id, thread);
-- 
-- CREATE INDEX IF NOT EXISTS posts_thread_uid_idx
--   ON posts (thread, id);
-- 
CREATE INDEX IF NOT EXISTS posts_thread_path_idx
  ON posts (thread, path);

CREATE index posts_uid_path_idx
  ON posts (id, path);

CREATE INDEX posts_thread_parent_path_uid_idx
  ON posts (thread, parent, path, id);
-- 
-- CREATE INDEX posts_uid_thread_parent_idx
--   ON posts (id, thread, parent);
-- 
-- --=========== THREADS ===========
-- 
CREATE INDEX threads_slug_idx
  ON threads (slug);

CREATE INDEX threads_forums_idx
  ON threads (forum_id);
-- 
-- CREATE INDEX threads_users_idx
--   ON threads (user_id);
-- 
create index threads_forum_id_created_idx
  on threads (forum_id, created);
-- 
-- --=========== USERS ===========
-- 
CREATE INDEX users_nickname_idx
  ON users (nickname);

CREATE INDEX users_email_idx
  ON users (email);

CREATE INDEX users_nickname_collate_email_about_fullname_uid_idx
  ON users (nickname, about, email, fullname, user_id);
-- 
-- --=========== FORUM_FOR_USER ===========
-- 
CREATE INDEX users_for_forum_full_idx
  on forum_for_users (forum_id, user_id, nickname COLLATE "usc_basic", email, about, fullname);
-- 
-- --=========== VOTES ===========
-- 
-- CREATE INDEX vote_users_idx
--   ON votes (user_id);
-- 
-- CREATE INDEX vote_threads_idx
--   ON votes (thread_id);