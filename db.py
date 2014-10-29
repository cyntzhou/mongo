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
