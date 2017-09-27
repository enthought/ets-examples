
from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal
from skimage import img_as_float
from skimage.data import astronaut, coins, logo

from image_analysis.model.rgb_color_space import (
    rgb_color_space, rgba_color_space
)


class TestRGBColorSpace(TestCase):

    def test_rgb_to_rgb(self):
        data = astronaut()

        result = rgb_color_space.to_rgb(data)

        assert_array_equal(result, data)

    def test_rgba_to_rgb(self):
        data = logo()

        result = rgba_color_space.to_rgb(data)

        assert_array_equal(result, data)

    def test_rgb_from_rgb_with_rgb_data(self):
        data = astronaut()

        result = rgb_color_space.from_rgb(data)

        assert_array_equal(result, data)

    def test_rgb_from_rgb_with_rgba_data(self):
        data = logo()

        result = rgb_color_space.from_rgb(data)

        assert_array_equal(result, data[..., :3])

    def test_rgba_from_rgb_with_rgb_data(self):
        data = astronaut()
        expected = np.full(data.shape[:-1] + (4,), 0xff, dtype='uint8')
        expected[..., :3] = data

        result = rgba_color_space.from_rgb(data)

        assert_array_equal(result, expected)

    def test_rgba_from_rgb_with_rgba_data(self):
        data = logo()

        result = rgba_color_space.from_rgb(data)

        assert_array_equal(result, data)

    def test_rgba_from_rgb_with_float_rgb_data(self):
        data = img_as_float(astronaut())
        expected = np.full(data.shape[:-1] + (4,), 1.0, dtype='float64')
        expected[..., :3] = data

        result = rgba_color_space.from_rgb(data)

        assert_array_equal(result, expected)

    def test_rgb_from_rgb_with_greyscale_data(self):
        data = coins()

        with self.assertRaises(ValueError):
            rgba_color_space.from_rgb(data)
