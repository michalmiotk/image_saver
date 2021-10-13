import pytest
import numpy as np

from main import is_pixel_in_threshold,  get_pixel_interval, calculate_percent_of_different_pixels


def test_is_pixel_in_threshold_EXPECTED_it_is():
    assert is_pixel_in_threshold(np.array([100, 100, 100]), np.array([80, 80, 80]), 30) == True

def test_is_pixel_in_threshold_EXPECTED_it_is_not():
    assert is_pixel_in_threshold(np.array([100, 100, 100]), np.array([80, 80, 80]), 5) == False

def test_get_pixel_interval():
    img = np.zeros((100,100,3))

    steps_width = 20
    steps_height = 10
    interval = get_pixel_interval(img.shape, steps_width=steps_width, steps_height=steps_height)
    assert interval['width'] == 5 and interval['height'] == 10

def test_calculate_percent_of_different_pixels():
    calculated_percent = calculate_percent_of_different_pixels(100, 100, 100)
    assert calculated_percent == 1