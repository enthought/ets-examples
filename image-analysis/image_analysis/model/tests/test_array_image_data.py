
from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal
from skimage import img_as_ubyte

from image_analysis.model.array_image_data import ArrayImageData
from image_analysis.model.rgb_color_space import (
    rgb_color_space, rgba_color_space
)


def dummy_color_map(data):
    """ Put the image into the red channel. """
    result = np.full(data.shape+(3,), 0xff, dtype='uint8')
    result[..., 0] = img_as_ubyte(data)
    return result


class TestArrayImageData(TestCase):

    def test_colour_space(self):
        image_data = ArrayImageData(np.zeros(shape=(10, 20, 30)))

        self.assertIsNone(image_data.color_space)

    def test_colour_space_rgb(self):
        image_data = ArrayImageData(np.zeros(shape=(10, 20, 30, 3)))

        self.assertEqual(image_data.color_space, rgb_color_space)

    def test_colour_space_rgba(self):
        image_data = ArrayImageData(np.zeros(shape=(10, 20, 30, 4)))

        self.assertEqual(image_data.color_space, rgba_color_space)

    def test_n_dim(self):
        image_data = ArrayImageData(
            data=np.zeros(shape=(10, 20, 30, 3)),
            color_space=rgb_color_space,
        )

        self.assertEqual(image_data.n_dim, 3)

    def test_n_dim_greyscale(self):
        image_data = ArrayImageData(
            data=np.zeros(shape=(10, 20, 30)),
            color_space=None,
        )

        self.assertEqual(image_data.n_dim, 3)

    def test_size(self):
        image_data = ArrayImageData(
            data=np.zeros(shape=(10, 20, 30, 3)),
            color_space=rgb_color_space,
        )

        self.assertEqual(image_data.size, (10, 20, 30))

    def test_size_greyscale(self):
        image_data = ArrayImageData(
            data=np.zeros(shape=(10, 20, 30)),
            color_space=None,
        )

        self.assertEqual(image_data.size, (10, 20, 30))

    def test_type(self):
        image_data = ArrayImageData(
            data=np.zeros(shape=(10, 20, 30, 3)),
        )

        self.assertEqual(image_data.type, np.dtype(float))

    def test_range_rgb_uint8(self):
        image_data = ArrayImageData(
            data=np.zeros(shape=(10, 20, 30, 3), dtype='uint8'),
            color_space=rgb_color_space,
        )

        assert_array_equal(image_data.range[0], [0x00, 0x00, 0x00])
        assert_array_equal(image_data.range[1], [0xff, 0xff, 0xff])

    def test_range_rgb_int8(self):
        image_data = ArrayImageData(
            data=np.zeros(shape=(10, 20, 30, 3), dtype='int8'),
            color_space=rgb_color_space,
        )

        assert_array_equal(image_data.range[0], [-0x80, -0x80, -0x80])
        assert_array_equal(image_data.range[1], [0x7f, 0x7f, 0x7f])

    def test_range_rgb_float(self):
        image_data = ArrayImageData(
            data=np.zeros(shape=(10, 20, 30, 3)),
            color_space=rgb_color_space,
        )

        assert_array_equal(image_data.range[0], [0.0, 0.0, 0.0])
        assert_array_equal(image_data.range[1], [1.0, 1.0, 1.0])

    def test_range_rgb_float_negative(self):
        data = np.zeros(shape=(10, 20, 30, 3))
        data[5, 5, 5, 1] = -0.5
        image_data = ArrayImageData(
            data=data,
            color_space=rgb_color_space,
        )

        assert_array_equal(image_data.range[0], [-1.0, -1.0, -1.0])
        assert_array_equal(image_data.range[1], [1.0, 1.0, 1.0])

    def test_range_greyscale_float(self):
        image_data = ArrayImageData(
            data=np.zeros(shape=(10, 20, 30)),
            color_space=None,
        )

        assert_array_equal(image_data.range[0], 0.0)
        assert_array_equal(image_data.range[1], 1.0)
        self.assertEqual(image_data.range[0].shape, ())
        self.assertEqual(image_data.range[1].shape, ())

    def test_to_rgb_float(self):
        image_data = ArrayImageData(
            data=np.zeros(shape=(10, 20, 30, 3)),
            color_space=rgb_color_space,
        )

        rgb = image_data.to_rgb()

        assert_array_equal(rgb.dtype, np.dtype('uint8'))
        assert_array_equal(rgb, np.zeros(shape=(10, 20, 30, 3), dtype='uint8'))

    def test_to_rgba_float(self):
        image_data = ArrayImageData(
            data=np.zeros(shape=(10, 20, 30, 4)),
            color_space=rgb_color_space,
        )

        rgb = image_data.to_rgb()

        assert_array_equal(rgb.dtype, np.dtype('uint8'))
        assert_array_equal(rgb, np.zeros(shape=(10, 20, 30, 4), dtype='uint8'))

    def test_to_rgb_greyscale(self):
        image_data = ArrayImageData(
            data=np.zeros(shape=(10, 20, 30)),
            color_space=None,
        )

        rgb = image_data.to_rgb()

        assert_array_equal(rgb.dtype, np.dtype('uint8'))
        assert_array_equal(rgb, np.zeros(shape=(10, 20, 30, 3), dtype='uint8'))

    def test_to_rgb_greyscale_colormap(self):
        image_data = ArrayImageData(
            data=np.zeros(shape=(10, 20, 30)),
            color_space=None,
        )

        rgb = image_data.to_rgb(dummy_color_map)

        assert_array_equal(rgb.dtype, np.dtype('uint8'))
        assert_array_equal(rgb[..., 0],
                           np.zeros(shape=(10, 20, 30), dtype='uint8'))
        assert_array_equal(rgb[..., 1:],
                           np.full((10, 20, 30, 2), 0xff, dtype='uint8'))
