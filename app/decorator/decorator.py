from flask import request, jsonify
from firebase_admin import auth
from functools import wraps

def middleware_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            id_token = request.headers.get('Authorization').split(' ')[1]
            print(id_token)
            decode_token = auth.verify_id_token(id_token=id_token, clock_skew_seconds=10)
            return f(*args, **kwargs)
        except auth.ExpiredIdTokenError as e:
            print(e)
            return jsonify(error='Token da het han'), 400
        except auth.InvalidIdTokenError as e:
            print(e)
            return jsonify(error='Token khong hop le'), 400
        except Exception as e:
            print(e)
            return jsonify(error='Khong ton tai token'), 400
    
    return wrapper
        
