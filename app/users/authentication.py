from functools import wraps
from flask import request, jsonify
import jwt
from .. import app
import datetime
from ..database import query_db

def token_required(orig_fumc):
    @wraps(orig_fumc)
    def wrapper(*args, **kwargs):
        # request
        token = _check_token()
        
        if token is None:
            return jsonify({'message': 'token not provided'}), 401
        
        try:
            print(token)
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            user = query_db("SELECT * FROM users where email = ?", (data['email'],))[0]        
        except Exception as ex:
            print(ex.args[0])
            return jsonify({'message': 'token is invalid'}), 401
                
        return orig_fumc({"email": user[1], "password": user[-1], "id": user[0],
                          "first_name": user[2], "last_name": user[-2]}, *args, **kwargs)

    return wrapper

def _check_token():
    token = None
    if 'token' in request.headers:
        token = request.headers['token']
    
    return token
        

def referesh_token(func):
    @wraps(func)
    def wrapper(*args, **argv):
        token = _check_token()
        if token is None:
            return jsonify({'message': 'token not provided'}), 401

        try:
            # print(token)
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            # print(data)
            if data.get("email", None) is not None:
                user = query_db("SELECT * FROM users where email = ?", (data['email'],))
                if len(user) == 0:
                    return jsonify({'message': 'eamil was not valid provided'}), 401
        except jwt.ExpiredSignatureError as ex:
            print(ex.args[0])
            data = request.get_json()
            if data.get("email", None) is not None:
                user = query_db("SELECT * FROM users where email = ?", (data['email'],))
                if len(user) == 0:
                    return jsonify({'message': 'eamil was not valid provided'}), 401

                token = jwt.encode(
                    {'email': data['email'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=24*60)},
                    app.config['SECRET_KEY'])
            else:
                return jsonify({'message': 'eamil not provided'}), 401
        except Exception as ex:
            return jsonify({'message': ex.args[0]}), 400

        return func(token, *args, **argv)
        
    return wrapper 