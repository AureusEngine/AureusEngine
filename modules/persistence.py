import pickle
import os

SAVE_FILE = "pattern_data.pkl"
USER_FILE = "users.pkl"

def save_data(data, filename=SAVE_FILE):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_data(filename=SAVE_FILE):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return {}

def save_user_data(users, filename=USER_FILE):
    with open(filename, 'wb') as f:
        pickle.dump(users, f)

def load_user_data(filename=USER_FILE):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return {}