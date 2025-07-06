import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

firebase_app = None

def initialize_firebase():
    global firebase_app
    if not firebase_admin._apps:
        cred = credentials.Certificate(st.secrets["firebase"])
        firebase_app = firebase_admin.initialize_app(cred, {
            'databaseURL': "https://aureusengine-433eb-default-rtdb.firebaseio.com/"
        })

def sanitize_pattern(pattern_str):
    return ''.join(c for c in pattern_str.upper() if c in {'W', 'L', 'M'})

def upload_session_data(user_id, session_data):
    initialize_firebase()
    ref = db.reference(f"sessions/{user_id}")
    ref.set(session_data)

def retrieve_session_data(user_id):
    initialize_firebase()
    ref = db.reference(f"sessions/{user_id}")
    data = ref.get()
    return data if data else []

def upload_user_pattern(pattern_str):
    initialize_firebase()
    sanitized = sanitize_pattern(pattern_str)
    ref = db.reference("user_patterns")
    patterns = ref.get() or []
    if sanitized not in patterns:
        patterns.append(sanitized)
        ref.set(patterns)