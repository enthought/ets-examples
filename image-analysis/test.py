from skimage.data import astronaut, coins
from image_analysis.model.array_image_data import ArrayImageData
from image_analysis.model.image_namespace import ImageNamespace
from image_analysis.ui.image_view import ImageView

image_namespace = ImageNamespace(
    images={
        'coins': ArrayImageData(coins()),
        'astronaut':  ArrayImageData(astronaut())
    },
    active_image='coins'
)

model_view = ImageView(model=image_namespace)
model_view.configure_traits()
