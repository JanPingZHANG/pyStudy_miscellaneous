from PIL import Image,ImageFilter

kitten = Image.open('123.jpg')
blurryKitten = kitten.filter(ImageFilter.GaussianBlur)
blurryKitten.save('123_blurred.jpg')
blurryKitten.show()
