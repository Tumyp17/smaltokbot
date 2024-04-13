from pymongo import MongoClient
from datetime import datetime
from urllib.parse import quote_plus
from config_reader import config


# This file is used for reading and editing MongoDB database

# Connecting to MongoDB
client = MongoClient('localhost', 27017)
# Choosing the database
db = client['gh_coffee_db']


# This function checks if user has already been added to DB. And adds a new user, using his Telegram profile info.
def check_and_add_user(message, code):
    if db.users.find_one({'user_id': message.from_user.id}) is None:
        new_user = {
            'first_name': str(message.from_user.first_name),
            'last_name': str(message.from_user.last_name),
            'user_id': message.from_user.id,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'state': 'null',
            'tel': '+' + message.text,
            'balance': '0',
            'code': code
        }
        db.users.insert_one(new_user)
    return


# This function receives users current state. Used in Aiogram filters.
def get_current_state(user_id):
    user = db.users.find_one({'user_id': user_id})
    return user['state']


# Receives a first name from DB
def get_first_name(user_id):
    user = db.users.find_one({'user_id': user_id})
    return user['first_name']


# Receives a last name from DB
def get_last_name(user_id):
    user = db.users.find_one({'user_id': user_id})
    return user['last_name']


# Receives a phone number from DB
def get_tel(user_id):
    user = db.users.find_one({'user_id': user_id})
    return user['tel']


def get_reg_times(user_id):
    user = db.users.find_one({'user_id': user_id})
    return user['reg']


# Receives users current balance from DB
def get_balance(user_id):
    user = db.users.find_one({'user_id': user_id})
    return user['balance']


# Updates users state in DB
def set_state(user_id, state_value):
    db.users.update_one({'user_id': user_id}, {"$set": {'state': state_value}})


# Updates users balance
def topup(user_id, state_value):
    db.users.update_one({'user_id': user_id}, {"$set": {'balance': state_value}})


# Deletes user from DB
def delete_user(user_id):
    db.users.delete_one({'user_id': user_id})


# Creates a url for CRM. Used in requests.
def get_bx_url(message, req_type):
    title = 'FIELDS[TITLE]=' + quote_plus(str(req_type + message.data))
    first_name = '&FIELDS[NAME]=' + quote_plus(str(message.from_user.first_name))
    last_name = '&FIELDS[LAST_NAME]=' + quote_plus(str(message.from_user.last_name))
    tel = '&FIELDS[PHONE][0][VALUE]=' + str(get_tel(message.from_user.id))
    user_id = '&FIELD[USERID][VALUE]=' + str(message.from_user.id)
    bitrix_url = str(config.bitrix_api.get_secret_value() + title + tel + first_name + last_name + user_id)
    return bitrix_url


# Creates another type of url for CRM
def get_bx_url_assistance(message, req_type):
    title = 'FIELDS[TITLE]=' + quote_plus(str(req_type + message.text))
    first_name = '&FIELDS[NAME]=' + quote_plus(str(message.from_user.first_name))
    last_name = '&FIELDS[LAST_NAME]=' + quote_plus(str(message.from_user.last_name))
    tel = '&FIELDS[PHONE][0][VALUE]=' + str(get_tel(message.from_user.id))
    user_id = '&FIELD[USERID][VALUE]=' + str(message.from_user.id)
    bitrix_url = str(config.bitrix_api.get_secret_value() + title + tel + first_name + last_name + user_id)
    return bitrix_url


# Receives an SMS code, that has been sent to user from DB
def get_code(user_id):
    user = db.users.find_one({'user_id': user_id})
    return user['code']
