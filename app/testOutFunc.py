from AIEngine.ED_algo import stream_to_multilabel
from AIEngine.TrOCR import image_to_stream
from PIL import Image

image = Image.open('C:/Users/Ghayth Ali/Desktop/Grad_Project/Server/RXReader-server/AIEngine/ghtest3.jpg')

print(stream_to_multilabel(image_to_stream(image)))
