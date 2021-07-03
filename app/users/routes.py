from flask import Blueprint, make_response, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from ..database import query_db
from .make_responses import make_400_reponse
import datetime
from .. import app
from .authentication import token_required, referesh_token
import random

users = Blueprint('users', __name__)

@users.route('/user/<user_id>', methods=['GET'])
@token_required
def get_user_by_id(user, user_id):
    try:
        u = query_db("SELECT * FROM users WHERE id = ?", (user_id,))[0]
    except Exception as ex:
        return jsonify({"message": ex.args[0]}), 500
    else:
        print(u)
        return jsonify({"email": u[1], "password": u[-1], "id": u[0],
                        "first_name": u[2], "last_name": u[-2]}), 200
         
@users.route('/user/<public_id>', methods=["PUT"])
@token_required
def update_user_info(user, public_id):
    try:
        u = query_db("SELECT * FROM users WHERE id = ?", (public_id,))[0]
    except Exception as ex:
        return jsonify({"message": ex.args[0]}), 500
    else:
        data = request.get_json()
        query_str, ll = "UPDATE users SET ", []
        if data.get("password", None) is not None:
            hashed_password = generate_password_hash(data['password'], method='sha256')
            query_str += "password = ?, "; ll.append(hashed_password)
        if data.get("email", None) is not None:
            query_str += "email = ?,"; ll.append(data.get("email"))
        if data.get("first_name", None) is not None:
            query_str += "first_name = ?,"; ll.append(data.get("first_name"))
        if data.get("last_name", None) is not None:
            query_str += "last_name = ?"; ll.append(data.get("last_name"))
            
        query_db(query_str, ll, com=True)
    
        return jsonify({"message": "user successfully updated!."}), 200

@users.route("/user/<public_id>", methods=["DELETE"])
@token_required
def delete_user_info(_, public_id):
    try:
        query_db("DELETE FROM users WHERE id = ?", (public_id,), com=True)
    except Exception as ex:
        return jsonify({"message": ex.args[0]}), 500
    else:
        return jsonify({"message": "delete was successfull"}), 202
    

@users.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data.get("email", None) is not None:
        user = query_db("SELECT * FROM users where email = ?", [data.get("email")])
        if len(user) == 0:
            return make_400_reponse("user not exists")
        # user[0][-1] give password user[0][1] give email
        if check_password_hash(user[0][-1], data.get("password", None)):
            token = jwt.encode(
                {'email': user[0][1], 
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=24*60)},
                app.config['SECRET_KEY'])
            return jsonify({'token': token})
    
    return make_response(jsonify({"message": "email or password was not correct!."}), 403)

@users.route("/user", methods=['GET'])
@token_required
def get_user(user):
    print(user)
    return jsonify({'user': user}), 200

@users.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    print(data)
    if data.get('email', None) is not None:
        users = query_db("SELECT * FROM users WHERE email = ?", (data["email"],))
        if len(users) != 0:
            return make_400_reponse("email already registered!.")
    else:
        return make_400_reponse("please provide email field")
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    query_db(
        """INSERT INTO users(email, password, first_name, last_name) VALUES (?, ?, ?, ?)""",
        (data["email"], hashed_password, data['first_name'], data['last_name']), com=True)
    token = jwt.encode(
            {'email': data['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=24*60)},
            app.config['SECRET_KEY'])
    
    return make_response(jsonify({'token': token}), 200)


@users.route('/referesh_token', methods=['POST'])
@referesh_token
def token_referesh(token):
    return jsonify({'token': token}), 200

@users.route('/user/photo', methods=['POST'])
@token_required
def save_photo(user):
    # print(user)
    user_id = user["id"]
    img = request.get_json().get("image", None)
    if img is None:
        return jsonify({"message": "image not provided"}), 400
    
    name = request.get_json().get("name", None)
    if name is None:
        name = "image_" + str(random.randint(0, 10000))
    
    q = query_db("INSERT INTO picture(img, name, user_id) VALUES (?, ?, ?)",
                 args=(img, name, user_id), com=True)
    print(q)
    
    return jsonify({"message": "picture successfully saved!."}), 200

@users.route('/user/photo', methods=['GET'])
@token_required
def get_photos(user):
    out = query_db("SELECT img, name FROM picture WHERE user_id = ?", args=(user["id"],))
    output = []
    for o in out:
        output.append({
            "image": o[0],
            "name": o[-1]
        })
    return jsonify({"result": output}), 200