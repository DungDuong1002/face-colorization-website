import tensorflow as tf
from tensorflow.keras.utils import img_to_array
import numpy as np
from PIL import Image
import cv2

def convert_image(input_image):
    # Load model
    model = tf.keras.models.load_model('D:\colorize_face_web\mysite\colorweb\my_models\colorize_face_model.h5', compile=False)
    # Preprocess the input image
    SIZE = 128
    print(input_image)
    # input_image = np.array(Image.open(io.BytesIO(input_image)).convert('RGB'))
    input_image = np.array(Image.open(input_image).convert('RGB'))
    org_h, org_w, _ = input_image.shape
    input_image = cv2.resize(input_image, (SIZE, SIZE))
    input_image = img_to_array(input_image.astype('float32') / 255.0)
    # Convert image
    output_image = np.clip(model.predict(input_image.reshape(1,SIZE, SIZE,3)),0.0,1.0).reshape(SIZE, SIZE,3)
    output_image = cv2.resize(output_image, (org_w, org_h))
    output_image = (output_image * 255.0).astype(np.uint8)
    output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
    # Convert the output image to a byte stream
    output_image = Image.fromarray(output_image)
    # output_image_bytes = io.BytesIO()
    # output_image.save(output_image_bytes, format='JPEG')
    # output_image_bytes = output_image_bytes.getvalue()
    return output_image