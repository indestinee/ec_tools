import numpy as np


def bytes_to_img(data: bytes) -> np.ndarray:
    import cv2
    np_arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img


def random_image(size=(256, 256, 3)):
    return np.random.randint(256, size=size, dtype=np.uint8)
