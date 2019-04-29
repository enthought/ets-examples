# Copyright (c) 2017, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
This module provides some functions for outputting the state of a cellular
automaton as images.  This relies on PIL/Pillow for saving the images.
"""
import os

import numpy as np
from PIL import Image


def save_image(automaton, filename, palette=None):
    """ Save an automaton as an image.

    Parameters
    ----------
    automaton : CellularAutomaton instance
        The automaton to use to create the image.
    filename : path
        The path to the file that will be used to save the image.
    palette : array of shape (N, 3)
        An array of N RGB values to use for the color of each state.
    """

    array = automaton.states
    if array.ndim >= 2:
        raise ValueError("Can only save image of 1D or 2D automaton.")
    _save_2d_image(array, filename, palette)


def save_image_sequence(recorder, filename, palette=None, duration=50):
    """ Save a recorded sequence of states as an image.

    For 1D automata this will produce a single 2D image showing the evolution
    with later states below earlier states.  For 2D automata this will produce
    either an animated GIF if the file extension is ``".gif"`` or a sequence
    of individual 2D images otherwise.

    Parameters
    ----------
    recorder : AutomataRecorder instance
        The automaton to use to create the image.
    filename : path
        The path to the file that will be used to save the image.
    palette : array of shape (N, 3)
        An array of N RGB values to use for the color of each state.
    duration : int
        The number of milliseconds for each frame in animated output.
    """

    base, ext = os.path.splitext(filename)
    if recorder.automaton.states.ndim == 1:
        array = np.array(recorder.record)
        _save_2d_image(array, filename, palette)
    elif ext == '.gif':
        _save_animated_gif(recorder.record, filename, palette, duration)
    else:
        arrays = recorder.record
        ndigits = len(str(arrays))
        template = base + '_{:0' + str(ndigits) + 'd}' + ext
        for i, array in enumerate(arrays):
            filename = template.format(i)
            _save_2d_image(array, filename, palette)


def _save_2d_image(array, filename, palette=None):
    mode = 'L' if palette is None else 'P'
    image = Image.fromarray(array, mode)
    if mode == 'P':
        palette = np.array(palette, dtype='uint8').ravel()
        image.putpalette(palette)

    image.save(filename)


def _save_animated_gif(arrays, filename, palette=None, duration=50):
    mode = 'L' if palette is None else 'P'
    images = []
    for array in arrays:
        image = Image.fromarray(array, mode)
        if mode == 'P':
            palette = np.array(palette, dtype='uint8').ravel()
            image.putpalette(palette.tobytes())
        images.append(image)

    images[0].save(
        filename, save_all=True, append_images=images[1:], optimize=True,
        duration=duration
    )
