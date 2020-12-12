import Information_Retrieval as IR
from PIL import Image

img_path = input('Enter Image Full Path: ')
input_img = Image.open(img_path)
images = IR.get_similar(input_img)
for img_name in images:
    img = IR.get_image(img_name)
    img.show()
