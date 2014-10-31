import datetime

from pymongo import MongoClient

client = MongoClient()
db = client['facebook']
users = db['users']


def new_user(user_params):
    user_id = users.insert(user_params)
    return user_id


def find_user(criteria):
    user = users.find_one(criteria)
    return user


def update_user(criteria, changeset):
    db.users.update(criteria, changeset)


def touch_user_login_time(criteria):
    update_user(criteria, {'last_login_at': datetime.datetime.now()})


def touch_user_logout_time(criteria):
    update_user(criteria, {'last_logout_at': datetime.datetime.now()})
