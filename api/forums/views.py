from flask import Blueprint, request, make_response, jsonify
from enquiry.connect import *
from enquiry.queries_db import *
from enquiry.secondary import *

# create new blueprint
forums_blueprint = Blueprint('forums', 'forums', url_prefix='/forum')


@forums_blueprint.route('/create', methods=['POST'])
def create_forum():
    content = request.get_json(silent=True)
    slug = content['slug']
    title = content['title']
    user_nickname = content['user']

    connect = connectDB()
    cursor = connect.cursor()
    select_command = 'SELECT * FROM users WHERE nickname = %s;'
    cursor.execute(select_command, [user_nickname, ])

    if cursor.rowcount == 0:
        cursor.close()

        return make_response(jsonify({}), 404)

    user_nickname = cursor.fetchone()[1]
    # в данной части кода можно сделать оптимизацию
    # (вместо поиска имени форума нужно сделать вставку данных и если она сработает)
    # то все прошло нормально, иначе выкинуть 409 ошибку
    select_command = 'SELECT * FROM forums WHERE slug = %s;'
    cursor.execute(select_command, [slug,])

    if cursor.rowcount:
        forum_data = cursor.fetchone()
        forum_id = forum_data[0]
        user_id = forum_data[1]
        slug = forum_data[2]
        title = forum_data[3]

        select_command = '''SELECT count(*) as posts_count FROM posts 
                            WHERE forum_id = %s;'''
        cursor.execute(select_command, [forum_id,])
        posts = cursor.fetchone()[0]

        select_command = '''SELECT nickname FROM users 
                            WHERE user_id = %s;'''
        cursor.execute(select_command, [user_id,])
        user = cursor.fetchone()[0]

        select_command = '''SELECT count(*) as threads_count FROM threads 
                            WHERE forum_id = %s;'''
        cursor.execute(select_command, [forum_id,])
        threads = cursor.fetchone()[0]

        param_name_array = ["posts", "slug", "threads", "title", "user"]
        param_value_array = [posts, slug, threads, title, user]
        exist_forum_data = dict(zip(param_name_array, param_value_array))
        cursor.close()

        return make_response(jsonify(exist_forum_data), 409)
    else:
        select_command = '''SELECT user_id FROM users 
                            WHERE nickname = %s;'''
        cursor.execute(select_command, [user_nickname,])
        user_id = cursor.fetchone()[0]

        insert_command = '''INSERT INTO forums (user_id, slug, title)
				            VALUES (%s, %s, %s);'''

        cursor.execute(insert_command, [user_id, slug, title,])
        connect.commit()

        param_name_array = ["posts", "slug", "threads", "title", "user"]
        param_value_array = [0, slug, 0, title, user_nickname]
        created_forum_data = dict(zip(param_name_array, param_value_array))
        cursor.close()

        return make_response(jsonify(created_forum_data), 201)


@forums_blueprint.route('/<slug>/create', methods=['POST'])
def create_thread(slug):
    content = request.get_json(silent=True)
    param_name_array = []
    param_value_array = []

    if 'author' in content:
        user_nickname = content['author']
        param_name_array.append('author')
        param_value_array.append(user_nickname)

    if 'created' in content:
        created = content['created']
        param_name_array.append('created')
        param_value_array.append(created)

    if 'message' in content:
        message = content['message']
        param_name_array.append('message')
        param_value_array.append(message)

    if 'title' in content:
        title = content['title']
        param_name_array.append('title')
        param_value_array.append(title)

    slug_th = ''
    if 'slug' in content:
        slug_th = content['slug']
        param_name_array.append('slug')
        param_value_array.append(slug_th)

    connect = connectDB()
    cursor = connect.cursor()
    is_thread_exist = False

    cursor.execute(SELECT_USERS_BY_NICKNAME, [param_value_array[0], ])

    if (cursor.rowcount == 0):
        cursor.close()

        return make_response(jsonify({"message": "Can't find user with nickname = %s \n" % param_value_array[0]}), 404)

    user_id = cursor.fetchone()[0]

    cursor.execute(SELECT_FORUM_BY_SLUG, [slug, ])

    if (cursor.rowcount == 0):
        cursor.close()

        return make_response(jsonify({"message": "Can't find forum with slug = %s\n" % slug}), 404)

    forum_id = cursor.fetchone()[0]

    try:

        if 'created' in param_name_array:
            if 'slug' in content:
                cursor.execute(INSERT_THREAD, [forum_id, user_id, param_value_array[1],
                                               param_value_array[2], slug_th, param_value_array[3], ])
            else:
                cursor.execute(INSERT_THREAD_WITHOUT_SLUG, [forum_id, user_id, param_value_array[1],
                                                            param_value_array[2], param_value_array[3], ])
        else:
            if 'slug' in param_name_array:
                cursor.execute(INSERT_THREAD_WITHOUT_CREATED,
                               [forum_id, user_id, param_value_array[1], slug_th, param_value_array[2], ])
            else:
                cursor.execute(INSERT_THREAD_WITHOUT_CREATED_AND_SLUG,
                               [forum_id, user_id, param_value_array[1], param_value_array[2], ])

        connect.commit()

        thread_id = cursor.fetchone()[0]

        cursor.execute(SELECT_FORUM_BY_FORUM_ID, [forum_id, ])
        forum = cursor.fetchone()[2]

        # param_name_array = ["author", "created", "forum", "id", "message", "slug", "title", "votes"]
        # param_value_array = [author, created, forum, thread_id, message, slug, title, 0]
        param_name_array.append('forum')
        param_value_array.append(forum)
        param_name_array.append('id')
        param_value_array.append(thread_id)
        exist_forum_data = dict(zip(param_name_array, param_value_array))
        cursor.close()

        return make_response(jsonify(exist_forum_data), 201)
    except psycopg2.DatabaseError as e:
        print('Error %s' % e)
        select_command = '''SELECT * FROM threads WHERE slug = %s'''
        cursor.execute(select_command, [slug,])

        [thread_id, forum_id, user_id, created, message, slug, title] = cursor.fetchone()[:]
        select_command = 'SELECT nickname FROM users WHERE user_id = %s;'
        cursor.execute(select_command, [user_id, ])
        author = cursor.fetchone()[0]

        select_command = 'SELECT slug FROM forums WHERE forum_id = %s;'
        cursor.execute(select_command, [forum_id, ])
        forum = cursor.fetchone()[0]

        select_command = 'SELECT count(*) as votes_count FROM votes WHERE thread_id = %s;'
        cursor.execute(select_command, [forum_id, ])
        votes = cursor.fetchone()[0]

        param_name_array = ["author", "created", "forum", "id", "message", "slug", "title", "votes"]
        param_value_array = [author, created, forum, thread_id, message, slug, title, votes]
        exist_forum_data = dict(zip(param_name_array, param_value_array))
        cursor.close()

        return make_response(jsonify(exist_forum_data), 409)


@forums_blueprint.route('/<slug>/details', methods=['GET'])
def get_forum_information(slug):
    connect = connectDB()
    cursor = connect.cursor()

    cursor = queries(cursor, SELECT_FORUM_BY_SLUG, [slug, ])

    if(cursor.rowcount == 0):
        cursor.close()

        return make_response(jsonify({ "message": "Can't find forum with slug = %s\n" % slug}), 404)

    [forum_id, user_id, slug, title] = cursor.fetchone()[:]
    cursor.execute(COUNT_POSTS_BY_FORUM_ID, [forum_id, ])
    posts = cursor.fetchone()[0]
    cursor.execute(COUNT_THREADS_BY_FORUM_ID, [forum_id, ])
    threads = cursor.fetchone()[0]
    cursor.execute(SELECT_USER_BY_USER_ID, [user_id, ])
    user = cursor.fetchone()[1]

    param_name_array = ["posts", "slug", "threads", "title", "user"]
    param_value_array = [posts, slug, threads, title, user]
    exist_forum_data = dict(zip(param_name_array, param_value_array))
    cursor.close()

    return make_response(jsonify(exist_forum_data), 200)


@forums_blueprint.route('/<slug>/threads', methods=['GET'])
def get_list_of_thread(slug):
    connect = connectDB()
    cursor = connect.cursor()

    cursor.execute(SELECT_FORUM_BY_SLUG, [slug, ])
    if cursor.rowcount == 0:
        cursor.close()

        return make_response(jsonify({ "message": "Can't find forum with slug = %s\n" % slug}), 404)

    forum_id = cursor.fetchone()[0]

    limit = ' ALL '
    if 'limit' in request.args:
        limit = request.args.get('limit')
    order = 'asc'
    if 'desc' in request.args:
        order = 'desc' if request.args.get('desc') == 'true' else 'asc'
    since = ''
    if 'since' in request.args:
        znak = ' <= ' if order == 'desc' else ' >= '
        since = 'and created ' + znak + "'" + request.args.get('since') + "'"

    order = ' ' + order + ' '
    slug = "'" + slug + "'"

    query = SELECT_THREADS_BY_FORUM_ID % (forum_id, since, order, limit)
    cursor.execute(query)

    threads = []
    param_array = ['author', 'created', 'forum', 'id', 'message', 'slug', 'title', 'votes']
    res = cursor.fetchall()
    for thread in res:
        cursor.execute(SELECT_USER_BY_USER_ID, [thread[2], ])
        author = cursor.fetchone()[1]
        forum = slug
        cursor.execute(COUNT_VOTES_BY_THREAD_ID, [thread[0], ])
        votes = cursor.fetchone()[0]
        id = thread[0]
        created = convert_time(thread[3])

        param_value_array = [author, created, forum, id, thread[4], thread[5], thread[6], votes]
        threads.append(dict(zip(param_array, param_value_array)))
    cursor.close()

    return make_response(jsonify(threads), 200)


@forums_blueprint.route('/<slug>/users', methods=['GET'])
def get_list_of_users(slug):
    connect = connectDB()
    cursor = connect.cursor()

    cursor = queries(cursor, SELECT_FORUM_BY_SLUG, [slug, ])
    if cursor.rowcount == 0:

        return make_response(jsonify({ "message": "Can't find forum with slug = %s\n" % slug}), 404)

    limit = ' ALL '
    if 'limit' in request.args:
        limit = request.args.get('limit')
    order = 'asc'
    if 'desc' in request.args:
        order = 'desc' if request.args.get('desc') == 'true' else 'asc'
    since = ''
    if 'since' in request.args:
        znak = ' <= ' if order == 'desc' else ' >= '
        since = 'and created ' + znak + "'" + request.args.get('since') + "'"

    forum_id = queries(cursor, SELECT_FORUM_BY_SLUG, [slug, ], 0)
    users = queries(cursor, UNION_TABLES, [])
    # ??????????????????


    return 'goodbye'
