from functools import wraps
from flask import request, jsonify
import jwt
from .. import app

def token_required(orig_fumc):
    @wraps(orig_fumc)
    def wrapper(*args, **kwargs):
        # request
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if token is None:
            return jsonify({'message': 'token is missing!!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            # current_user = User.query.filter_by(public_id=data['public_id']).first()
            current_user = None
        except:
            return jsonify({'message': 'token is invalid'}), 401
                
        return orig_fumc(current_user, *args, **kwargs)

    return wrapper