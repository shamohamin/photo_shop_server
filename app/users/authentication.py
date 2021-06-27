from functools import wraps
from flask import request, jsonify
import jwt
from .. import app
from ..database import query_db

def token_required(orig_fumc):
    @wraps(orig_fumc)
    def wrapper(*args, **kwargs):
        # request
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        
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