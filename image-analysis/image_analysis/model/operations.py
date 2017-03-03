
from skimage import filters
from .simple_operation import SimpleOperation, is_greyscale
from .parameters import MaskParameters


# Filters
prewitt = SimpleOperation(
    function=filters.prewitt,
    parameters=MaskParameters,
    is_available=is_greyscale,
)

prewitt_h = SimpleOperation(
    function=filters.prewitt_h,
    name='prewitt horizontal',
    parameters=MaskParameters,
    is_available=is_greyscale,
)

prewitt_v = SimpleOperation(
    function=filters.prewitt_v,
    name='prewitt vertical',
    parameters=MaskParameters,
    is_available=is_greyscale,
)

rank_order = SimpleOperation(
    function=filters.rank_order,
    parameters=None
)

roberts = SimpleOperation(
    function=filters.roberts,
    parameters=MaskParameters,
    is_available=is_greyscale,
)

sobel = SimpleOperation(
    function=filters.sobel,
    parameters=MaskParameters,
    is_available=is_greyscale,
)
