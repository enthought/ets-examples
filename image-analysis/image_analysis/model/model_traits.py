from __future__ import absolute_import

from numpy import dtype

from traits.api import Array, Enum, Int, Tuple


#: An rgb24 or rgba32 array
RgbArray = Array(shape=(None, None, (3, 4)), dtype='uint8')

#: Allowed channel dtypes
DType = Enum(dtype('uint8'), dtype('float'), dtype('int64'))

#: A size in pixels.
Size = Tuple(Int, Int)
