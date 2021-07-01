import cv2
from flask import Blueprint, jsonify, make_response
from .utility_funcs import filter_credential_cheker, filter_photo_checker_and_defaultier, apply_filters
import base64

filters = Blueprint('filters', __name__)

@filters.route('/filters', methods=['POST'])
@filter_credential_cheker
@filter_photo_checker_and_defaultier
def apply_filter(decoded_image, attributes):
    try:
        filtered_image = apply_filters(decoded_image, attributes)
        print(filtered_image)
        cv2.imwrite("a.png", filtered_image)
        with open("a.png", 'rb') as f:
            my_string = base64.b64encode(f.read())
        print(len(my_string))
        return jsonify({"image": my_string.decode('utf-8')}), 200
    except Exception as ex:
        return jsonify({"message": ex.args[0]}), 500