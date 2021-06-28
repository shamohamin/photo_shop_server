import cv2
from flask import Blueprint, jsonify, make_response
from .utility_funcs import filter_credential_cheker, filter_photo_checker_and_defaultier, apply_filters

filters = Blueprint('filters', __name__)

@filters.route('/filters', methods=['POST'])
@filter_credential_cheker
@filter_photo_checker_and_defaultier
def apply_filter(decoded_image, attributes):
    try:
        filtered_image = apply_filters(decoded_image, attributes)
        print(filtered_image)
        cv2.imwrite("a.png", filtered_image)
        # encoding image
        
    except Exception as ex:
        return jsonify({"message": ex.args[0]}), 500
    
    return make_response({'response': 'ok'}, 200)