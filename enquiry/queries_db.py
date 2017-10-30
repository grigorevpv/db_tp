COUNT_POSTS_BY_FORUM_ID = '''SELECT count(*) as posts_count FROM posts 
                            WHERE forum_id = %s;'''

COUNT_THREADS_BY_FORUM_ID = '''SELECT count(*) as threads_count FROM threads 
                               WHERE forum_id = %s;'''

COUNT_VOTES_BY_THREAD_ID = '''SELECT sum(voice) as votes_count FROM votes 
                                WHERE thread_id = %s;'''

SELECT_USER_BY_USER_ID = '''SELECT * FROM users
                                WHERE user_id = %s;'''

SELECT_USERS_BY_FORUM_ID = '''SELECT user_id FROM %s 
                                WHERE forum_id = %s'''

SELECT_USERS_BY_NICKNAME = '''SELECT * FROM users 
                                WHERE nickname = %s'''

SELECT_USERS_BY_NICKNAME_OR_EMAIL = '''SELECT * FROM users 
                                        WHERE nickname = %s OR email = %s'''

UPDATE_USER_BY_NICKNAME = '''UPDATE users SET about = %s, email = %s, fullname = %s
                                WHERE nickname = %s'''

INSERT_USER = '''INSERT INTO users (nickname, about, email, fullname) 
                    VALUES (%s, %s, %s, %s)'''

SELECT_FORUM_BY_SLUG = '''SELECT * FROM forums
                            WHERE slug = %s;'''

SELECT_FORUM_BY_FORUM_ID = '''SELECT * FROM forums
                                WHERE forum_id = %s;'''

SELECT_THREAD_BY_SLUG = '''SELECT * FROM threads WHERE slug = %s'''

SELECT_THREADS_BY_FORUM_ID = '''SELECT * FROM threads
                                WHERE forum_id = %s %s
                                ORDER BY created %s
                                LIMIT %s;'''

INSERT_THREAD = '''INSERT INTO threads (forum_id, user_id, created, message, slug, title)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING *'''

INSERT_THREAD_WITHOUT_CREATED = '''INSERT INTO threads (forum_id, user_id, message, slug, title)
                                    VALUES (%s, %s, %s, %s, %s) RETURNING *'''

INSERT_THREAD_WITHOUT_SLUG = '''INSERT INTO threads (forum_id, user_id, created, message, title)
                                VALUES (%s, %s, %s, %s, %s) RETURNING *'''

INSERT_THREAD_WITHOUT_CREATED_AND_SLUG = '''INSERT INTO threads (forum_id, user_id, message, title)
                                            VALUES (%s, %s, %s, %s) RETURNING *'''

SELECT_USERS = '''SELECT * FROM users WHERE user_id IN (SELECT u.user_id FROM posts p
                 JOIN users u ON p.user_id = u.user_id
                 WHERE forum_id = %s
                 UNION
                 SELECT us.user_id FROM threads th
                 JOIN users us ON th.user_id = us.user_id
                 WHERE forum_id = %s) AND users.nickname < %s
                 ORDER BY users.nickname COLLATE ucs_basic %s 
                 LIMIT %s;'''