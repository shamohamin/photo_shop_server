from flask import Blueprint, jsonify, make_response
from .utility_funcs import filter_credential_cheker, filter_photo_checker_and_defaultier

filters = Blueprint('filters', __name__)

@filters.route('/filters', methods=['POST'])
@filter_credential_cheker
@filter_photo_checker_and_defaultier
def apply_filter(decoded_image, attributes):
    return make_response({'response': 'ok'}, 200)