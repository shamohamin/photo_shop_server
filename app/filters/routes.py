import cv2
from flask import Blueprint, jsonify, make_response, request
from .utility_funcs import filter_credential_cheker, filter_photo_checker_and_defaultier, apply_filters
import base64
from ..database import query_db

filters = Blueprint('filters', __name__)

@filters.route('/filters', methods=['POST'])
@filter_credential_cheker
@filter_photo_checker_and_defaultier
def apply_filter(decoded_image, attributes):
    try:
        filtered_image = apply_filters(decoded_image, attributes)
        cv2.imwrite("a.png", filtered_image)
        with open("a.png", 'rb') as f:
            my_string = base64.b64encode(f.read())
        print(len(my_string))
        out = query_db("SELECT description from filter where name = ?",
                 args=(request.get_json().get("filter_type"),))
        return jsonify({"image": my_string.decode('utf-8'), "des": out[0][0]}), 200
    except Exception as ex:
        return jsonify({"message": ex.args[0]}), 500