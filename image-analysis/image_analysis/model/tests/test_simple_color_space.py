
from unittest import TestCase

from numpy.testing import assert_array_equal
from skimage.color import rgb2hsv, hsv2rgb
from skimage.data import astronaut, coins, logo

from image_analysis.model.simple_color_space import hsv_color_space


class TestSimpleColorSpace(TestCase):

    def test_hsv_to_rgb(self):
        data = rgb2hsv(astronaut())
        expected = hsv2rgb(data)

        result = hsv_color_space.to_rgb(data)

        assert_array_equal(result, expected)

    def test_hsv_from_rgb_with_rgb_data(self):
        data = astronaut()

        result = hsv_color_space.from_rgb(data)

        assert_array_equal(result, rgb2hsv(data))

    def test_hsv_from_rgb_with_rgba_data(self):
        data = logo()

        result = hsv_color_space.from_rgb(data)

        assert_array_equal(result, rgb2hsv(data[..., :3]))

    def test_hsv_from_rgb_with_greyscale_data(self):
        data = coins()

        with self.assertRaises(ValueError):
            hsv_color_space.from_rgb(data)
