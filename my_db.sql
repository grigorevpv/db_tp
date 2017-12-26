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
  user_id  INTEGER REFERENCES users (user_id) ON DELETE CASCADE NOT NULL,
  forum_id INTEGER REFERENCES forums (forum_id) ON DELETE CASCADE NOT NULL
);

ALTER TABLE forum_for_users
    ADD CONSTRAINT forum_for_users_cstr
    UNIQUE(user_id, forum_id);

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
  INSERT INTO forum_for_users (user_id, forum_id)
  (
    SELECT NEW.user_id, NEW.forum_id
    FROM users
    WHERE users.user_id = new.user_id
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

