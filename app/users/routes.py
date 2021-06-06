from flask import Blueprint, make_response, jsonify, request

users = Blueprint('users', __name__)

@users.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    pass

@users.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    
    if not auth or not auth.password or not auth.username:
        return make_response('Could not ', 
                            401, {'WWW-authntication': 'Basic realm="Login required!"'})
    # user = User.query.filter_by(name=auth.username).first()
    # if not user:
        # return make_response('Could not ', 
                            # 401, 
                            # {'WWW-authntication': 'Basic realm="Login required!"'})
    # print('awli')
    # if check_password_hash(user.password, auth.password):
    #     token = jwt.encode(
    #         {'public_id': user.public_id, 
    #         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
    #         app.config['SECRET_KEY'])
    #     return jsonify({'token': token.decode('utf-8')})
    
    return make_response('Could not ', 
                        401, 
                        {'WWW-authntication': 'Basic realm="Login required!"'})

@users.route('/user', methods=['POST'])
def create_user():
    print(request.data)
    pass