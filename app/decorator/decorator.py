from flask import request, jsonify
from firebase_admin import auth
from functools import wraps

def middleware_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            id_token = request.headers.get('Authorization').split(' ')[1]
            decode_token = auth.verify_id_token(id_token=id_token, clock_skew_seconds=10)
            return f(*args, **kwargs)
        except auth.ExpiredIdTokenError as e:
            print(e)
            return jsonify(message='Token da het han'), 400
        except auth.InvalidIdTokenError as e:
            print(e)
            return jsonify(message='Token khong hop le'), 400
        
    
    return wrapper
        
