
SELECT_USER_BY_USER_ID = '''SELECT users.user_id, users.nickname, users.about, users.email, users.fullname
								FROM users
								WHERE user_id = %s;'''

SELECT_USERS_BY_FORUM_ID = '''SELECT user_id FROM %s 
                                WHERE forum_id = %s;'''

SELECT_USERS_BY_NICKNAME = '''SELECT users.user_id, users.nickname, users.about, users.email, users.fullname
                              FROM users 
                              WHERE users.nickname = %s;'''

SELECT_USERS_BY_NICKNAME_OR_EMAIL = '''SELECT users.user_id, users.nickname, users.about, users.email, users.fullname 
                                         FROM users WHERE users.nickname = %s OR users.email = %s;'''

UPDATE_USER_BY_NICKNAME = '''UPDATE users SET about = %s, email = %s, fullname = %s
                                WHERE nickname = %s
                                RETURNING users.user_id, users.nickname, users.about, users.email, users.fullname;'''

INSERT_USER = '''INSERT INTO users (nickname, about, email, fullname) 
                    VALUES (%s, %s, %s, %s) 
                    RETURNING users.user_id, users.nickname, users.about, users.email, users.fullname;'''

SELECT_USERS_SINCE_DESC = '''SELECT * FROM users WHERE user_id IN (SELECT u.user_id FROM posts p
                 JOIN users u ON p.user_id = u.user_id
                 WHERE forum_id = %s
                 UNION
                 SELECT us.user_id FROM threads th
                 JOIN users us ON th.user_id = us.user_id
                 WHERE forum_id = %s) AND users.nickname < '%s'
                 ORDER BY users.nickname COLLATE ucs_basic DESC 
                 LIMIT %s;'''

SELECT_USERS_SINCE = '''SELECT * FROM users WHERE user_id IN (SELECT u.user_id FROM posts p
                 JOIN users u ON p.user_id = u.user_id
                 WHERE forum_id = %s
                 UNION
                 SELECT us.user_id FROM threads th
                 JOIN users us ON th.user_id = us.user_id
                 WHERE forum_id = %s) AND users.nickname > '%s'
                 ORDER BY users.nickname COLLATE ucs_basic 
                 LIMIT %s;'''

SELECT_USERS = '''SELECT * FROM users WHERE user_id IN (SELECT u.user_id FROM posts p
                 JOIN users u ON p.user_id = u.user_id
                 WHERE forum_id = %s
                 UNION
                 SELECT us.user_id FROM threads th
                 JOIN users us ON th.user_id = us.user_id
                 WHERE forum_id = %s)
                 ORDER BY users.nickname COLLATE ucs_basic 
                 LIMIT %s;'''

SELECT_USERS_DESC = '''SELECT * FROM users WHERE user_id IN (SELECT u.user_id FROM posts p
                 JOIN users u ON p.user_id = u.user_id
                 WHERE forum_id = %s
                 UNION
                 SELECT us.user_id FROM threads th
                 JOIN users us ON th.user_id = us.user_id
                 WHERE forum_id = %s)
                 ORDER BY users.nickname COLLATE ucs_basic DESC 
                 LIMIT %s;'''

SELECT_COUNT_USERS = '''SELECT count(*) as users_count FROM users;'''

DELETE_USERS_TABLE = '''DELETE FROM users;'''

