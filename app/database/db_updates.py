from pymongo import MongoClient
from datetime import datetime

# This file is used for adding updates from user to MongoDB

# Connecting to MongoDB
client = MongoClient('localhost', 27017)
# Choosing the database
db = client['gh_coffee_db']


# Adding message update to MongoDB
def add_update(message):
    new_update = {
        'first_name': str(message.from_user.first_name),
        'last_name': str(message.from_user.last_name),
        'user_id': message.from_user.id,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'text': message.text,
        'seconds': (datetime.now() - datetime(1, 1, 1, 0, 0)).total_seconds(),
        'message_id': int(message.message_id),
        'type': 'message'
    }
    db.updates.insert_one(new_update)


# Adding callback update to MongoDB
def add_update_callback(callback):
    new_update = {
        'first_name': str(callback.from_user.first_name),
        'last_name': str(callback.from_user.last_name),
        'user_id': callback.from_user.id,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'text': callback.data,
        'seconds': (datetime.now() - datetime(1, 1, 1, 0, 0)).total_seconds(),
        'message_id': int(callback.callback_id),
        'type': 'callback'
    }
    db.updates.insert_one(new_update)


# This function is used to receive how much time has passed since the last update from user.
# It is used for the timeup function and to prevent bot from handling too many updates in a short amount of time
def get_seconds(user_id, current):
    user = None
    i = current
    while user is None:
        user = db.updates.find_one({'user_id': user_id, 'message_id': int(i - 1)})
        if user is None and i == current:
            user = current - 10
            return user
        i -= 1
    if user is not None:
        return user['seconds']
    else:
        return False
