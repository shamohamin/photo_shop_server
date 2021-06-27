from flask import make_response, jsonify

def make_400_reponse(message):
    return make_response(
                jsonify({'message': f'{message}'}),
                400
            )

def make_201_response(message):
    return make_response(jsonify({'message': f'{message}'}), 201)