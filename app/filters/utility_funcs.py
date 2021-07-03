from functools import wraps
from flask import request, jsonify, make_response
import base64
from PIL import Image
from io import BytesIO
import numpy as np
import cv2


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
            decoded_image = decoded_image[:, :, -1::-1]
            attribute = which_filter_is(request.get_json().get('filter_type', None))
            attribute['filter_type'] = request.get_json().get('filter_type', None)
            print(attribute)
        except Exception as ex:
            return make_response(jsonify({'message': ex.args[0]}, 500))
        
        return f(decoded_image, attribute, *args, **kwargs)
    return wrapper
        
def decoding_image(encode_image):
    image_decoded = base64.b64decode(encode_image)
    img = Image.open(BytesIO(image_decoded))
    # img.show()
    img_m = np.asarray(img.convert("RGB"))
    return img_m

def which_filter_is(filter_type):
    attributes = {'kernel_size': request.get_json().get('kernel_size', 3)}    
    if filter_type == "gussian_filter":
        attributes['sigma'] = request.get_json().get('sigma', None)
    elif filter_type == "bilateral_filter":
        attributes['sigma_space'] = request.get_json().get('sigma_space', None)
        attributes['sigma_color'] = request.get_json().get('sigma_color', None)
    else:
        if filter_type != 'box_filter':
            raise Exception("Please choose existing filters")
    return attributes


def apply_filters(img, attributes):
    filter_type = attributes['filter_type']
    kernel_size = attributes['kernel_size']
    photo = None
    if filter_type == "box_filter":
        photo = apply_linear_filter(img, kernel_size)
    elif filter_type == "gussian_filter":
        photo = apply_guassian_filter(img, kernel_size, attributes.get('sigma', None))
    elif filter_type == "bilateral_filter":
        photo = apply_bilateral_filter(img, kernel_size,
                                      attributes.get('sigma_color', None),
                                      attributes.get('sigma_space', None))
    if not isinstance(photo, np.ndarray):
        raise Exception("somtehing went wrong!")
    return photo

def apply_linear_filter(img, kernel_size):
    filtered_img = cv2.boxFilter(img, -1, (kernel_size, kernel_size))
    
    return filtered_img

def apply_guassian_filter(img, kernel_size, sigma=0):
    filtered_img = cv2.GaussianBlur(img,
                                    (kernel_size, kernel_size),
                                    sigma if sigma is not None else 0)
    return filtered_img
    

def apply_bilateral_filter(img, kernel_size, sigmaColor=0.3, sigmaSpace=25):
    sigmaColor = sigmaColor if sigmaColor is not None else 0.3
    sigmaSpace = sigmaSpace if sigmaSpace is not None else 25
    filtered_img = cv2.bilateralFilter(img, kernel_size, sigmaColor, sigmaSpace)
    return filtered_img