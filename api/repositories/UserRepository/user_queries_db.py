
SELECT_USER_BY_USER_ID = '''SELECT * FROM users
                                WHERE user_id = %s;'''

SELECT_USERS_BY_FORUM_ID = '''SELECT user_id FROM %s 
                                WHERE forum_id = %s;'''

SELECT_USERS_BY_NICKNAME = '''SELECT * FROM users 
                                WHERE nickname = %s;'''

SELECT_USERS_BY_NICKNAME_OR_EMAIL = '''SELECT users.user_id, users.nickname, users.about, users.email, users.fullname 
                                         FROM users WHERE nickname = %s OR email = %s;'''

UPDATE_USER_BY_NICKNAME = '''UPDATE users SET about = %s, email = %s, fullname = %s
                                WHERE nickname = %s;'''

INSERT_USER = '''INSERT INTO users (nickname, about, email, fullname) 
                    VALUES (%s, %s, %s, %s) 
                    RETURNING users.user_id, users.nickname, users.about, users.email, users.fullname;'''
