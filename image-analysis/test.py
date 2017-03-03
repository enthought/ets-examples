from skimage.data import astronaut, coins
from image_analysis.model.array_image_data import ArrayImageData
from image_analysis.model.image import Image
from image_analysis.ui.image_view import ImageView

image_data = ArrayImageData(astronaut())
image_data = ArrayImageData(coins(), color_space=None)
image = Image(image_data=image_data, name='astronaut')

model_view = ImageView(model=image)
model_view.configure_traits()
