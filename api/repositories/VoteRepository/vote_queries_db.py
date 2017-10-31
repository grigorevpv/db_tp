INSERT_VOTE = '''INSERT INTO votes (user_id, thread_id, voice) 
                    VALUES (%s, %s, %s) 
                    RETURNING votes.vote_id, votes.user_id, votes.thread_id, votes.voice;'''

SELECT_VOTE_BY_THREAD_AND_USER_ID = '''SELECT votes.vote_id, votes.user_id, votes.thread_id, votes.voice
                                         FROM votes WHERE thread_id = %s AND user_id = %s;'''

COUNT_VOTES_BY_THREAD_ID = '''SELECT sum(votes.voice) FROM votes WHERE thread_id = %s GROUP BY votes.thread_id;'''

UPDATE_VOTE = '''UPDATE votes SET voice = %s WHERE votes.user_id = %s AND votes.thread_id = %s
                    RETURNING votes.vote_id, votes.user_id, votes.thread_id, votes.voice;'''

SELECT_COUNT_VOTES = '''SELECT count(*) as votes_count FROM votes;'''

DELETE_VOTES_TABLE = '''DELETE FROM votes;'''
