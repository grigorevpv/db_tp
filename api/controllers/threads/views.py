from datetime import datetime
from flask import Blueprint, request, make_response, jsonify
from psycopg2.extras import execute_values

from api.repositories.connect import PostgresDataContext
from api.repositories.ThreadRepository.thread_queries_db import *
from api.repositories.ForumRepository.forum_queries_db import *
from api.repositories.PostRepository.post_queries_db import *
from api.repositories.VoteRepository.vote_queries_db import *
from enquiry.queries_db import *
from enquiry.secondary import *

# create new blueprint
threads_blueprint = Blueprint('threads', 'threads', url_prefix='/api/thread')

data_context = PostgresDataContext()
STATUS_CODE = {
    'OK': 200,
    'CREATED': 201,
    'NOT_FOUND': 404,
    'CONFLICT': 409
}


@threads_blueprint.route('/<slug_or_id>/create', methods=['POST'])
def create_posts(slug_or_id):
    content = request.get_json(silent=True)
    connect, cursor = data_context.create_connection()
    thread = None

    if slug_or_id.isdigit():
        cursor.execute(SELECT_THREAD_BY_ID, [slug_or_id, ])
        thread = cursor.fetchone()
        if thread is None:
            data_context.put_connection(connect)
            cursor.close()
            return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
                                 STATUS_CODE['NOT_FOUND'])
    else:
        cursor.execute(SELECT_THREAD_BY_SLUG, [slug_or_id, ])
        thread = cursor.fetchone()
        if thread is None:
            data_context.put_connection(connect)
            cursor.close()
            return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
                                 STATUS_CODE['NOT_FOUND'])

    created_threads_arr = []
    created_time = datetime.now()

    data = []
    query = "INSERT INTO posts (id, user_id, thread, forum_id, parent, created, message, path, author, forum) VALUES %s"

    for post in content:
        cursor.execute(SELECT_USERS_BY_NICKNAME, [post['author']])
        user = cursor.fetchone()
        if user is None:
            data_context.put_connection(connect)
            cursor.close()
            return make_response(jsonify({"message": "Can't find user with nickname: " + post['author']}),
                                 STATUS_CODE['NOT_FOUND'])

        post_path = list()
        parent_id = 0
        if post.get('parent') is not None:
            parent_id = post['parent']
            cursor.execute(SELECT_POST_BY_ID, [post['parent'], ])
            parent_post = cursor.fetchone()
            if parent_post is None:
                data_context.put_connection(connect)
                cursor.close()
                return make_response(jsonify({"message": "Parent post was created in another thread"}),
                                     STATUS_CODE['CONFLICT'])
            else:
                if parent_post["thread"] == thread["id"]:
                    post_path.extend(parent_post["path"])
                else:
                    data_context.put_connection(connect)
                    cursor.close()
                    return make_response(jsonify({"message": "Parent post was created in another thread"}),
                                         STATUS_CODE['CONFLICT'])

        cursor.execute(SELECT_NEXT_VAL)
        post_id = cursor.fetchone()["nextval"]
        post_path.append(post_id)

        data.append([post_id, user["user_id"], thread["id"], thread["forum_id"], parent_id, created_time,
                     post["message"], post_path, user["nickname"], thread["forum"], ])

        created_thread_data = {
            "author": user["nickname"],
            "created": convert_time(created_time),
            "forum": thread["forum"],
            "id": post_id,
            "isEdited": False,
            "message": post["message"],
            "parent": parent_id,
            "thread": thread["id"]
        }

        created_threads_arr.append(created_thread_data)

    execute_values(cursor, query, data)
    cursor.execute(INCREMENT_POSTS_BY_NUMBER, [len(data), thread["forum_id"], ])

    data_context.put_connection(connect)
    cursor.close()
    return make_response(jsonify(created_threads_arr), STATUS_CODE['CREATED'])


@threads_blueprint.route('/<slug_or_id>/vote', methods=['POST'])
def create_vote(slug_or_id):
    content = request.get_json(silent=True)
    connect, cursor = data_context.create_connection()

    try:
        if slug_or_id.isdigit():
            cursor.execute(INSERT_VOTE_BY_THREAD_ID, [content['nickname'], slug_or_id, content['voice']], )
            data = cursor.fetchone()
            if data is None:
                data_context.put_connection(connect)
                cursor.close()
                return make_response(jsonify({"message": "Can't find thread or user"}),
                                     STATUS_CODE['NOT_FOUND'])

        else:
            cursor.execute(INSERT_VOTE_BY_THREAD_SLUG, [content['nickname'], slug_or_id, content['voice']], )
            data = cursor.fetchone()
            if data is None:
                data_context.put_connection(connect)
                cursor.close()
                return make_response(jsonify({"message": "Can't find thread or user"}),
                                     STATUS_CODE['NOT_FOUND'])

        # Получаем значение поля thread
        cursor.execute(SELECT_THREAD_BY_ID, [data['thread_id'], ])
        thread = cursor.fetchone()
        thread["created"] = convert_time(thread["created"])
        data_context.put_connection(connect)
        cursor.close()
        return make_response(jsonify(thread), STATUS_CODE['OK'])

    except:
        data_context.put_connection(connect)
        cursor.close()
        return make_response(jsonify({"message": "Can't find thread or user"}),
                             STATUS_CODE['NOT_FOUND'])


# @threads_blueprint.route('/<slug_or_id>/vote', methods=['POST'])
# def create_vote(slug_or_id):
# 	content = request.get_json(silent=True)
# 	connect, cursor = data_context.create_connection()
#
# 	if slug_or_id.isdigit():
# 		cursor.execute(SELECT_THREAD_BY_ID, [slug_or_id, ])
# 		thread = cursor.fetchone()
# 		if thread is None:
# 			data_context.put_connection(connect)
# 			cursor.close()
# 			return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
# 								 STATUS_CODE['NOT_FOUND'])
# 	else:
# 		cursor.execute(SELECT_THREAD_BY_SLUG, [slug_or_id, ])
# 		thread = cursor.fetchone()
# 		if thread is None:
# 			data_context.put_connection(connect)
# 			cursor.close()
# 			return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
# 								 STATUS_CODE['NOT_FOUND'])
#
# 	cursor.execute(SELECT_USERS_BY_NICKNAME, [content["nickname"]])
# 	user = cursor.fetchone()
# 	if user is None:
# 		data_context.put_connection(connect)
# 		cursor.close()
# 		return make_response(jsonify({"message": "Can't find user with nickname: " + content["nickname"]}),
# 		                     STATUS_CODE['NOT_FOUND'])
#
# 	cursor.execute(SELECT_VOTE_BY_THREAD_AND_USER_ID, [thread["id"], user["user_id"]])
# 	vote = cursor.fetchone()
# 	if vote is None:
# 		cursor.execute(INSERT_VOTE, [user["user_id"], thread["id"], content["voice"], ])
# 		vote = cursor.fetchone()
# 	else:
# 		if vote["voice"] != content["voice"]:
# 			cursor.execute(UPDATE_VOTE, [content["voice"], user["user_id"], thread["id"], ])
# 			vote = cursor.fetchone()
#
# 	cursor.execute(COUNT_VOTES_BY_THREAD_ID, [thread["id"], ])
# 	count_votes = cursor.fetchone()["votes_count"]
#
# 	thread["votes"] = count_votes
# 	thread["created"] = convert_time(thread["created"])
#
# 	data_context.put_connection(connect)
# 	cursor.close()
# 	return make_response(jsonify(thread), STATUS_CODE['OK'])


@threads_blueprint.route('/<slug_or_id>/details', methods=['GET'])
def get_thread_information(slug_or_id):
    connect, cursor = data_context.create_connection()

    if slug_or_id.isdigit():
        cursor.execute(SELECT_THREAD_BY_ID, [slug_or_id, ])
        thread = cursor.fetchone()
        if thread is None:
            data_context.put_connection(connect)
            cursor.close()
            return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
                                 STATUS_CODE['NOT_FOUND'])
    else:
        cursor.execute(SELECT_THREAD_BY_SLUG, [slug_or_id, ])
        thread = cursor.fetchone()
        if thread is None:
            data_context.put_connection(connect)
            cursor.close()
            return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
                                 STATUS_CODE['NOT_FOUND'])

    cursor.execute(COUNT_VOTES_BY_THREAD_ID, [thread["id"], ])
    count_votes = cursor.fetchone()["votes_count"]

    thread["votes"] = count_votes
    thread["created"] = convert_time(thread["created"])

    data_context.put_connection(connect)
    cursor.close()
    return make_response(jsonify(thread), STATUS_CODE['OK'])


@threads_blueprint.route('/<slug_or_id>/details', methods=['POST'])
def update_thread_information(slug_or_id):
    content = request.get_json(silent=True)
    connect, cursor = data_context.create_connection()

    if slug_or_id.isdigit():
        cursor.execute(SELECT_THREAD_BY_ID, [slug_or_id, ])
        thread = cursor.fetchone()
        if thread is None:
            data_context.put_connection(connect)
            cursor.close()
            return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
                                 STATUS_CODE['NOT_FOUND'])
    else:
        cursor.execute(SELECT_THREAD_BY_SLUG, [slug_or_id, ])
        thread = cursor.fetchone()
        if thread is None:
            data_context.put_connection(connect)
            cursor.close()
            return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
                                 STATUS_CODE['NOT_FOUND'])

    if 'message' not in content:
        content['message'] = thread['message']
    if 'title' not in content:
        content['title'] = thread['title']

    command = '''UPDATE threads SET message = '%s', title = '%s'
								WHERE id = %s RETURNING *;''' % (content['message'], content['title'], thread["id"])
    cursor.execute(command)
    thread = cursor.fetchone()
    thread["created"] = convert_time(thread["created"])

    data_context.put_connection(connect)
    cursor.close()
    return make_response(jsonify(thread), STATUS_CODE['OK'])


@threads_blueprint.route('/<slug_or_id>/posts', methods=['GET'])
def get_posts_information(slug_or_id):
    params = request.args
    connect, cursor = data_context.create_connection()
    if slug_or_id.isdigit():
        command = SELECT_THREAD_BY_ID % (int(slug_or_id))
        cursor.execute(command)
        thread = cursor.fetchone()

        if thread is None:
            data_context.put_connection(connect)
            cursor.close()
            return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
                                 STATUS_CODE['NOT_FOUND'])
    else:
        cursor.execute(SELECT_THREAD_BY_SLUG, [slug_or_id, ])
        thread = cursor.fetchone()
        if thread is None:
            data_context.put_connection(connect)
            cursor.close()
            return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
                                 STATUS_CODE['NOT_FOUND'])

    sort = params.get('sort')
    since = params.get('since')
    limit = params.get('limit')
    desc = params.get('desc')

    data = None

    try:
        if sort == 'flat' or sort is None:
            if limit is not None and since is None and desc is None:
                cursor.execute(FLAT_SORT_LIMIT, [thread['id'], limit])

            elif limit is not None and since is None and desc is not None:
                command = FLAT_SORT_LIMIT_DESC %(thread['id'], desc, desc, limit)
                # cursor.execute(FLAT_SORT_LIMIT_DESC, [thread['id'], desc, desc, limit])
                cursor.execute(command)

            elif limit is not None and since is not None and desc is None:
                cursor.execute(FLAT_SORT_SINCE_LIMIT, [thread['id'], since, limit])

            elif limit is not None and since is not None and desc is not None:
                command = FLAT_SORT_SINCE_LIMIT_DESC %(thread['id'], desc, since, since, desc, desc, limit)
                # cursor.execute(FLAT_SORT_SINCE_LIMIT_DESC, [thread['id'], desc, since, since, desc, desc, limit])
                cursor.execute(command)

            elif limit is None and since is None and desc is not None:
                cursor.execute(FLAT_SORT_DESC, [thread['id'], desc, desc])

            elif limit is None and since is None and desc is None:
                cursor.execute(FLAT_SORT, [thread['id']])

        elif sort == 'tree':
            if limit is not None and since is None and desc is None:
                cursor.execute(TREE_SORT_LIMIT, [thread['id'], limit])

            elif limit is not None and since is None and desc is not None:
                command = TREE_SORT_LIMIT_DESC %(thread['id'], desc, desc, limit)
                # cursor.execute(TREE_SORT_LIMIT_DESC, [thread['id'], desc, desc, limit])
                cursor.execute(command)

            elif limit is not None and since is not None and desc is None:
                cursor.execute(TREE_SORT_SINCE_LIMIT, [thread['id'], since, limit])

            elif limit is not None and since is not None and desc is not None:
                command = TREE_SORT_SINCE_LIMIT_DESC %(thread['id'], desc, since, since, desc, desc, limit)
                cursor.execute(command)
                # cursor.execute(TREE_SORT_SINCE_LIMIT_DESC, [thread['id'], desc, since, since, desc, desc, limit])

            elif limit is None and since is None and desc is not None:
                cursor.execute(TREE_SORT_DESC, [thread['id'], desc, desc])

            elif limit is None and since is None and desc is None:
                cursor.execute(TREE_SORT, [thread['id']])

        elif sort == 'parent_tree':
            if limit is not None and since is None and desc is None:
                cursor.execute(PARENT_SORT_LIMIT, [thread['id'], thread['id'], limit])

            elif limit is not None and since is None and desc is not None:
                command = PARENT_SORT_LIMIT_DESC %(thread['id'], thread['id'], desc, desc, limit, desc, desc)
                # cursor.execute(PARENT_SORT_LIMIT_DESC, [thread['id'], thread['id'], limit, desc, desc])
                cursor.execute(command)

            elif limit is not None and since is not None and desc is None:
                # command = PARENT_SORT_SINCE_LIMIT %(thread['id'], thread['id'], since, limit)
                cursor.execute(PARENT_SORT_SINCE_LIMIT, [thread['id'], thread['id'], since, limit])
                # cursor.execute(command)

            elif limit is not None and since is not None and desc is not None:
                command = PARENT_SORT_SINCE_LIMIT_DESC %(thread['id'], thread['id'], desc, since,
                                                                     since, desc, desc, limit, desc, desc)
                # cursor.execute(PARENT_SORT_SINCE_LIMIT_DESC, [thread['id'], thread['id'], desc, since,
                #                                                      since, desc, desc, limit, desc, desc])
                cursor.execute(command)

            elif limit is None and since is None and desc is not None:
                cursor.execute(PARENT_SORT_DESC, [thread['id'], desc, desc])

            elif limit is None and since is None and desc is None:
                cursor.execute(PARENT_SORT, [thread['id']])

    except:
        print('sort error')

    data = cursor.fetchall()

    for post in data:
        post["created"] = convert_time(post["created"])

    data_context.put_connection(connect)
    cursor.close()
    return make_response(jsonify(data), STATUS_CODE['OK'])


# @threads_blueprint.route('/<slug_or_id>/posts', methods=['GET'])
# def get_posts_information(slug_or_id):
#     params = request.args
#     connect, cursor = data_context.create_connection()
#     if slug_or_id.isdigit():
#         command = SELECT_THREAD_BY_ID % (int(slug_or_id))
#         cursor.execute(command)
#         thread = cursor.fetchone()
#
#         if thread is None:
#             data_context.put_connection(connect)
#             cursor.close()
#             return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
#                                  STATUS_CODE['NOT_FOUND'])
#     else:
#         cursor.execute(SELECT_THREAD_BY_SLUG, [slug_or_id, ])
#         thread = cursor.fetchone()
#         if thread is None:
#             data_context.put_connection(connect)
#             cursor.close()
#             return make_response(jsonify({"message": "Can't find thread with id: " + slug_or_id}),
#                                  STATUS_CODE['NOT_FOUND'])
#
#     limit = ' ALL '
#     if 'limit' in params:
#         limit = params.get('limit')
#     order = 'asc'
#     if 'desc' in params:
#         order = 'desc' if params.get('desc') == 'true' else 'asc'
#     since = 0
#     if 'since' in params:
#         since = params.get('since')
#     sort = 'flat'
#     if 'sort' in params:
#         sort = params.get('sort')
#     order = ' ' + order + ' '
#
#     posts = []
#     if sort == 'flat':
#         if since == 0:
#             command = '''SELECT author, created, forum, id, message, parent, thread FROM posts WHERE thread = %s ORDER BY created %s, id %s LIMIT %s;''' % (
#                 thread["id"], order, order, limit)
#             cursor.execute(command)
#             posts = cursor.fetchall()
#         else:
#             command = '''SELECT author, created, forum, id, message, parent, thread FROM posts WHERE thread = %s ORDER BY created %s, id %s;''' % (
#                 thread["id"], order, order)
#             cursor.execute(command)
#             posts = cursor.fetchall()
#             posts = posts_since_limit(posts, since, limit)
#     elif sort == 'tree':
#         if since == 0:
#             command = '''SELECT author, created, forum, id, message, parent, thread FROM posts WHERE thread = %s ORDER BY path %s, id %s LIMIT %s;''' % (
#                 thread["id"], order, order, limit)
#             cursor.execute(command)
#             posts = cursor.fetchall()
#         else:
#             command = '''SELECT author, created, forum, id, message, parent, thread FROM posts WHERE thread = %s ORDER BY path %s;''' % (
#                 thread["id"], order)
#             cursor.execute(command)
#             posts = cursor.fetchall()
#             posts = posts_since_limit(posts, since, limit)
#     elif sort == 'parent_tree':
#         if since == 0:
#             command = '''SELECT author, created, forum, id, message, parent, thread FROM posts WHERE path[1] IN (SELECT posts.id FROM posts
# 						 WHERE thread = %s AND parent = 0 ORDER BY id %s
# 						 LIMIT %s OFFSET %s) ORDER BY path %s;''' % (
#                 thread["id"], order, limit, since, order)
#             cursor.execute(command)
#             posts = cursor.fetchall()
#         else:
#             command = '''SELECT author, created, forum, id, message, parent, thread FROM posts WHERE path[1] IN (SELECT posts.id FROM posts
# 						 WHERE thread = %s AND parent = 0 ORDER BY id %s)
# 						 ORDER BY path %s;''' % (thread["id"], order, order)
#             cursor.execute(command)
#             posts = cursor.fetchall()
#             posts = posts_since_limit_parent(posts, params['since'], params['limit'])
#
#     post_arr = []
#     for post in posts:
#         post["created"] = convert_time(post["created"])
#         post_arr.append(post)
#
#     data_context.put_connection(connect)
#     cursor.close()
#     return make_response(jsonify(post_arr), STATUS_CODE['OK'])


def posts_since_limit(content, since, limit):
    for i in range(len(content) - 1):
        if content[i]["id"] == int(since):
            return content[i + 1:i + int(limit) + 1]
    return []


def posts_since_limit_parent(content, since, limit):
    for i in range(len(content) - 1):
        if content[i]["id"] == int(since):
            start = i + 1
            stop = start
            flag = 1
            for j in range(start, len(content) - 1):
                if content[j]["parent"] == 0:
                    flag += 1
                if flag > int(limit):
                    break
                stop += 1
            return content[start:stop + 2]
    return []
