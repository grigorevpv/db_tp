SELECT_THREADS_BY_FORUM_ID = '''SELECT threads.id, threads.forum_id, threads.user_id, 
										threads.created, threads.message, threads.slug, threads.title 
								FROM threads WHERE forum_id = %s %s ORDER BY created %s LIMIT %s;'''

COUNT_VOTES_BY_THREAD_ID = '''SELECT sum(voice) as votes_count FROM votes 
								WHERE thread_id = %s;'''

# SELECT_THREAD_BY_ID = '''SELECT threads.id, threads.forum_id, threads.user_id,
# 							threads.created, threads.message, threads.slug, threads.title
# 							FROM threads WHERE id = %s;'''

# SELECT_THREAD_BY_SLUG = '''SELECT threads.id, threads.forum_id, threads.user_id,
# 							threads.created, threads.message, threads.slug, threads.title
# 							FROM threads WHERE slug = %s;'''

SELECT_THREAD_BY_ID = '''SELECT *
							FROM threads WHERE threads.id = %s;'''

SELECT_THREAD_BY_SLUG = '''SELECT * 
							FROM threads WHERE slug = %s;'''

UPDATE_THREAD = '''UPDATE threads SET threads.message = %s, threads.title = %s
								WHERE threads.id = %s
								RETURNING threads.id, threads.forum_id, threads.user_id, 
										threads.created, threads.message, threads.slug, threads.title;'''

SELECT_COUNT_THREADS = '''SELECT count(*) as threads_count FROM threads;'''

DELETE_THREADS_TABLE = '''DELETE FROM threads;'''

SELECT_POST_BY_ID = '''SELECT posts.post_id, posts.user_id, posts.thread_id, posts.forum_id, posts.created, posts.isedited, posts.message, posts.parent_id, posts.path 
								FROM posts WHERE post_id = %s;'''

INSERT_VOTE_BY_THREAD_SLUG = '''
								INSERT INTO votes (user_id, thread_id, voice)
								    VALUES (
								                (
								                    SELECT users.user_id
								                    FROM users
								                    WHERE users.nickname = %s
								                ),
								                (
								                    SELECT threads.id
								                    FROM threads
								                    WHERE threads.slug = %s
								                ),
								                %s
								            )
    							ON CONFLICT ON CONSTRAINT vote_user_thread
							    DO UPDATE SET voice = EXCLUDED.voice
							    RETURNING votes.thread_id;
							    '''

INSERT_VOTE_BY_THREAD_ID = '''
								INSERT INTO votes (user_id, thread_id, voice)
								    VALUES (
								                (
								                    SELECT users.user_id
								                    FROM users
								                    WHERE users.nickname = %s
								                ),
								                %s,
								                %s
								            )
    							ON CONFLICT ON CONSTRAINT vote_user_thread
							    DO UPDATE SET voice = EXCLUDED.voice
							    RETURNING votes.thread_id;
							    '''

FLAT_SORT = '''
                SELECT posts.id, posts.thread, posts.forum, posts.author,
                  posts.parent, posts.message, posts.created, posts.isedited
                FROM posts
                WHERE posts.thread = %s
                ORDER BY posts.id;
            '''

FLAT_SORT_DESC = '''
                    SELECT posts.id, posts.thread, posts.forum, posts.author,
                      posts.parent, posts.message, posts.created, posts.isedited
                    FROM posts
                    WHERE posts.thread = %s
                    ORDER BY CASE %s
                                WHEN false THEN posts.id
                                ELSE NULL
                             END ASC,
                
                             CASE %s
                                WHEN true THEN posts.id
                                ELSE NULL
                             END DESC;  
                    '''

FLAT_SORT_LIMIT = '''
                    SELECT posts.id, posts.thread, posts.forum, posts.author,
                      posts.parent, posts.message, posts.created, posts.isedited
                    FROM posts
                    WHERE posts.thread = %s
                    ORDER BY posts.id
                    LIMIT %s;
                    '''

FLAT_SORT_LIMIT_DESC = '''
                            SELECT posts.id, posts.thread, posts.forum, posts.author,
                              posts.parent, posts.message, posts.created, posts.isedited
                            FROM posts
                            WHERE posts.thread = %s
                            ORDER BY CASE %s
                                        WHEN false THEN posts.id
                                        ELSE NULL
                                     END ASC,
                        
                                     CASE %s
                                        WHEN true THEN posts.id
                                        ELSE NULL
                                     END DESC
                            LIMIT %s;
                        '''

FLAT_SORT_SINCE_LIMIT = '''
                            SELECT posts.id, posts.thread, posts.forum, posts.author,
                              posts.parent, posts.message, posts.created, posts.isedited
                            FROM posts
                            WHERE posts.thread = %s AND posts.id > %s
                            ORDER BY posts.id
                            LIMIT %s;
                        '''

FLAT_SORT_SINCE_LIMIT_DESC = '''
                                SELECT posts.id, posts.thread, posts.forum, posts.author,
                                  posts.parent, posts.message, posts.created, posts.isedited
                                FROM posts
                                WHERE posts.thread = %s AND CASE %s
                                    WHEN false THEN posts.id > %s
                                    WHEN true  THEN posts.id < %s
                                END
                                ORDER BY CASE %s
                                            WHEN false THEN posts.id
                                            ELSE NULL
                                         END ASC,
                            
                                         CASE %s
                                            WHEN true THEN posts.id
                                            ELSE NULL
                                         END DESC
                                LIMIT %s;
                                '''

PARENT_SORT = '''
                SELECT posts.id, posts.thread, posts.forum, posts.author,
                    posts.parent, posts.message, posts.created, posts.isedited
                FROM posts
                WHERE posts.thread = %s
                ORDER BY posts.path;
                '''

PARENT_SORT_DESC = '''
                        SELECT posts.id, posts.thread, posts.forum, posts.author,
                          posts.parent, posts.message, posts.created, posts.isedited
                        FROM posts
                        WHERE posts.thread = %s
                        ORDER BY CASE %s
                                    WHEN false THEN posts.path
                                    ELSE NULL
                                 END ASC,
                    
                                 CASE %s
                                    WHEN true THEN  posts.path
                                    ELSE NULL
                                 END DESC;
                    '''

PARENT_SORT_LIMIT = '''
                        SELECT posts.id, posts.thread, posts.forum, posts.author,
                          posts.parent, posts.message, posts.created, posts.isedited
                        FROM posts
                        WHERE posts.thread = %s
                          AND posts.path[1] IN (
                                            SELECT p.path[1]
                                            FROM posts p
                                            WHERE p.thread = %s AND p.parent = 0
                                            ORDER BY p.id
                                            LIMIT %s
                                        )
                        ORDER BY posts.path;
                    '''

PARENT_SORT_LIMIT_DESC = '''
                            SELECT posts.id, posts.thread, posts.forum, posts.author,
                                posts.parent, posts.message, posts.created, posts.isedited
                            FROM posts
                            WHERE posts.thread = %s
                              AND posts.path[1] IN (
                                                SELECT p.path[1]
                                                FROM posts p
                                                WHERE p.thread = %s
                                                      AND p.parent = 0
                                                ORDER BY CASE %s
                                                            WHEN false THEN p.id
                                                            ELSE NULL
                                                         END ASC,
                        
                                                         CASE %s
                                                            WHEN true THEN  p.id
                                                            ELSE NULL
                                                         END DESC
                                                LIMIT %s
                                            )
                            ORDER BY CASE %s
                                        WHEN false THEN posts.path
                                        ELSE NULL
                                     END ASC,
                        
                                     CASE %s
                                        WHEN true THEN  posts.path
                                        ELSE NULL
                                     END DESC;
                            '''

PARENT_SORT_SINCE_LIMIT = '''
                                SELECT posts.id, posts.thread, posts.forum, posts.author,
                                    posts.parent, posts.message, posts.created, posts.isedited
                                FROM posts
                                WHERE posts.thread = %s
                                  AND posts.path[1] IN (
                                                    SELECT p.path[1]
                                                    FROM posts p
                                                    WHERE p.thread = %s
                                                          AND p.parent = 0
                                                          AND p.path > (
                                                                            SELECT pr.path
                                                                            FROM posts pr
                                                                            WHERE pr.id = %s
                                                                        )
                            
                                                    ORDER BY p.id
                                                    LIMIT %s
                                                )
                                ORDER BY posts.path;  
                            '''

PARENT_SORT_SINCE_LIMIT_DESC = '''
                                    SELECT posts.id, posts.thread, posts.forum, posts.author,
                                      posts.parent, posts.message, posts.created, posts.isedited
                                    FROM posts
                                    WHERE posts.thread = %s
                                      AND posts.path[1] IN (
                                                        SELECT pr.path[1]
                                                        FROM posts pr
                                                        WHERE pr.thread = %s
                                                              AND pr.parent = 0
                                                              AND CASE %s
                                                                      WHEN false THEN pr.path > (
                                                                                                 SELECT p_sub.path
                                                                                                 FROM posts p_sub
                                                                                                 WHERE p_sub.id = %s
                                                                                                )
                                                                      WHEN true  THEN pr.path < (
                                                                                                 SELECT p_sub.path
                                                                                                 FROM posts p_sub
                                                                                                 WHERE p_sub.id = %s
                                                                                                )
                                                              END
                                
                                                        ORDER BY CASE %s
                                                                    WHEN false THEN pr.id
                                                                    ELSE NULL
                                                                 END ASC,
                                
                                                                 CASE %s
                                                                    WHEN true THEN  pr.id
                                                                    ELSE NULL
                                                                 END DESC
                                                        LIMIT %s
                                                    )
                                    ORDER BY CASE %s
                                                WHEN false THEN posts.path
                                                ELSE NULL
                                             END ASC,
                                
                                             CASE %s
                                                WHEN true THEN  posts.path
                                                ELSE NULL
                                             END DESC;
                                '''

TREE_SORT = '''
                SELECT posts.id, posts.thread, posts.forum, posts.author,
                    posts.parent, posts.message, posts.created, posts.isedited
                FROM posts
                WHERE posts.thread = %s
                ORDER BY posts.path;
            '''

TREE_SORT_DESC = '''
                     SELECT posts.id, posts.thread, posts.forum, posts.author,
                        posts.parent, posts.message, posts.created, posts.isedited
                    FROM posts
                    WHERE posts.thread = %s
                    ORDER BY CASE %s
                                WHEN false THEN posts.path
                                ELSE NULL
                             END ASC,
                
                             CASE %s
                                WHEN true  THEN posts.path
                                ELSE NULL
                             END DESC;
                    '''

TREE_SORT_LIMIT = '''
                        SELECT posts.id, posts.thread, posts.forum, posts.author,
                            posts.parent, posts.message, posts.created, posts.isedited
                        FROM posts
                        WHERE posts.thread = %s
                        ORDER BY posts.path
                        LIMIT %s; 
                    '''

TREE_SORT_LIMIT_DESC = '''
                            SELECT posts.id, posts.thread, posts.forum, posts.author,
                                posts.parent, posts.message, posts.created, posts.isedited
                            FROM posts
                            WHERE posts.thread = %s
                            ORDER BY CASE %s
                                    WHEN false THEN posts.path
                                    ELSE NULL
                                 END ASC,
                            
                                 CASE %s
                                    WHEN true  THEN posts.path
                                    ELSE NULL
                                 END DESC
                            LIMIT %s;
                        '''

TREE_SORT_SINCE_LIMIT = '''
                                SELECT posts.id, posts.thread, posts.forum, posts.author,
                                    posts.parent, posts.message, posts.created, posts.isedited
                                FROM posts
                                WHERE posts.thread = %s AND posts.path > (SELECT p.path
                                                                              FROM posts p
                                                                              WHERE p.id = %s)
                                ORDER BY posts.path
                                LIMIT %s;
                        '''

TREE_SORT_SINCE_LIMIT_DESC = '''
                                SELECT posts.id, posts.thread, posts.forum, posts.author,
                                    posts.parent, posts.message, posts.created, posts.isedited
                                FROM posts
                                WHERE posts.thread = %s AND CASE %s
                                  
                                                                        WHEN false THEN posts.path > (
                                                                                                  SELECT p.path
                                                                                                  FROM posts p
                                                                                                  WHERE p.post_id = %s
                                                                                                 )
                                                                        WHEN true  THEN posts.path < (
                                                                                                  SELECT p.path
                                                                                                  FROM posts p
                                                                                                  WHERE p.post_id = %s
                                                                                                 )
                                                                    END
                                ORDER BY CASE %s
                                            WHEN false THEN posts.path
                                            ELSE NULL
                                         END ASC,
                            
                                         CASE %s
                                            WHEN true THEN  posts.path
                                            ELSE NULL
                                         END DESC
                                LIMIT %s;
                                '''