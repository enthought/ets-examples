
import numpy as np

from model.array_image_data import ArrayImageData


def flip(image, axis):
    """ Flip image data around the specified axis. """
    if image.is_grayscale():
        # shift flipping axis to avoid color channels
        axis -= 1
    result_data = np.flip(image.data, axis)
    result = ArrayImageData(data=result_data, color_space=image.color_space)
    return result
