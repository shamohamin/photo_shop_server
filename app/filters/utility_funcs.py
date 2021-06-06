from functools import wraps
from flask import request, jsonify, make_response
import base64
from PIL import Image
from io import BytesIO
import numpy as np

def filter_credential_cheker(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        filter_type = str(request.get_json().get('filter_type', None))
        image = str(request.get_json().get('image', None))
        if image is None or filter_type is None or \
                len(image) == 0 or len(filter_type) == 0:
            statement = 'photo' if image is None else 'filter_type'
            return make_response(
                jsonify({'message': f'{statement} field must be provided'}),
                400
            )
        return f(*args, **kwargs)
    
    return wrapper
        
def filter_photo_checker_and_defaultier(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        encoded_image = request.get_json().get('image', None)
        try:
            decoded_image = decoding_image(encoded_image)
            attribute = which_filter_is(request.get_json().get('filter_type', None))
        except Exception as ex:
            return make_response(jsonify({'message': ex.args[0]}, 500))
        
        return f(decoded_image, attribute, *args, **kwargs)
    return wrapper
        
def decoding_image(encode_image):
    image_decoded = base64.b64decode(encode_image)
    img = Image.open(BytesIO(image_decoded))
    img.show()
    img_m = np.asarray(img.convert("RGB"))
    
    return img_m

def which_filter_is(filter_type):
    attributes = {'kernel_size': request.get_json().get('kernel_size', None)}    
    if filter_type == "gussian":
        attributes['sigma'] = request.get_json().get('sigma', None)
    elif filter_type == "bilateral":
        attributes['sigma'] = request.get_json().get('sigma', None)
        attributes['sigma_color'] = request.get_json().get('sigma_color', None)
    else:
        if filter_type != 'linear':
            raise Exception("Please choose existing filters")
    return attributes