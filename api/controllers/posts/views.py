from flask import Blueprint, request, make_response, jsonify

from api.repositories.connect import PostgresDataContext
from api.repositories.UserRepository.user_queries_db import *
from api.repositories.ForumRepository.forum_queries_db import *
from api.repositories.ThreadRepository.thread_queries_db import *
from enquiry.queries_db import *
from enquiry.connect import *
from enquiry.secondary import *

# create new blueprint
posts_blueprint = Blueprint('posts', 'posts', url_prefix='/api/post')

data_context = PostgresDataContext()
STATUS_CODE = {
    'OK': 200,
    'CREATED': 201,
    'NOT_FOUND': 404,
    'CONFLICT': 409
}


@posts_blueprint.route('/<id>/details', methods=['GET'])
def get_post_details_get(id):
    params = request.args.getlist('related')
    connect, cursor = data_context.create_connection()

    command = '''SELECT * FROM posts WHERE id = %s;''' % (int(id))
    cursor.execute(command)
    post = cursor.fetchone()
    if post is None:
        data_context.put_connection(connect)
        cursor.close()
        return make_response(jsonify({"message": "Can't find post with id: " + id}),
                             STATUS_CODE['NOT_FOUND'])

    cursor.execute(SELECT_USER_BY_USER_ID, [post["user_id"], ])
    post_user = cursor.fetchone()
    if post_user is None:
        data_context.put_connection(connect)
        cursor.close()
        return make_response(jsonify({"message": "Can't find user with id: " + post["user_id"]}),
                             STATUS_CODE['NOT_FOUND'])

    cursor.execute(SELECT_FORUM_BY_FORUM_ID, [post["forum_id"], ])
    post_forum = cursor.fetchone()
    if post_forum is None:
        data_context.put_connection(connect)
        cursor.close()
        return make_response(jsonify({"message": "Can't find forum with id: " + post["forum_id"]}),
                             STATUS_CODE['NOT_FOUND'])

    user, forum, thread = ({}, {}, {})
    for val in params:
        for key in val.split(','):
            if 'user' == key:
                user = post_user
            if 'forum' == key:

                param_name_array = ["posts", "slug", "threads", "title", "user"]
                param_value_array = [post_forum['posts'], post_forum["slug"], post_forum['threads'],
                                     post_forum["title"], post_forum["user"]]
                forum = dict(zip(param_name_array, param_value_array))
            if 'thread' == key:
                cursor.execute(SELECT_THREAD_BY_ID, [post["thread"], ])
                thread = cursor.fetchone()
                if thread is None:
                    data_context.put_connection(connect)
                    cursor.close()
                    return make_response(jsonify({"message": "Can't find thread with id: " + post["thread"]}),
                                         STATUS_CODE['NOT_FOUND'])
                thread["created"] = convert_time(thread["created"])

    param_name_array = ["author", "created", "forum", "id", "isEdited", "message", "parent", "thread"]
    param_value_array = [post_user["nickname"], convert_time(post["created"]),
                         post_forum["slug"], post["id"], post["isedited"],
                         post["message"], post["parent"], post["thread"]]
    post = dict(zip(param_name_array, param_value_array))

    post_data = dict()

    if len(user) != 0:
        post_data['author'] = user
    if len(forum) != 0:
        post_data['forum'] = forum
    if len(thread) != 0:
        post_data['thread'] = thread
    post_data['post'] = post

    data_context.put_connection(connect)
    cursor.close()
    return make_response(jsonify(post_data), STATUS_CODE['OK'])


@posts_blueprint.route('/<id>/details', methods=['POST'])
def get_post_details_post(id):
    content = request.get_json(silent=True)
    connect, cursor = data_context.create_connection()

    command = '''SELECT * FROM posts WHERE id = %s;''' % (int(id))
    cursor.execute(command)
    post = cursor.fetchone()
    if post is None:
        data_context.put_connection(connect)
        cursor.close()
        return make_response(jsonify({"message": "Can't find post with id: " + id}),
                             STATUS_CODE['NOT_FOUND'])

    if 'message' in content:
        if post["message"] != content['message']:
            command = '''UPDATE posts SET message = '%s', isedited = %s
											WHERE id = %s RETURNING *;''' % (content['message'], True, post["id"])
            cursor.execute(command)
            post = cursor.fetchone()

    post["created"] = convert_time(post["created"])
    post["isEdited"] = post["isedited"]

    data_context.put_connection(connect)
    cursor.close()
    return make_response(jsonify(post), STATUS_CODE['OK'])
