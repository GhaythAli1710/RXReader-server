import base64
import io
from PIL import Image
from rest_framework.decorators import api_view
from rest_framework import status

from AIEngine.ED_algo import stream_to_multilabel
from AIEngine.TrOCR import image_to_stream
from app.models import test
from app.serializers import TestSerializer
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def testAPI(request):
    # GET
    if request.method == 'GET':
        tst = test.objects.all()
        ser = TestSerializer(tst, many=True)
        return Response(ser.data)
    # POST
    elif request.method == 'POST':
        ser = TestSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def receive_image(request):
    string = request.data['image']
    imgBytes = base64.b64decode(string)
    img = Image.open(io.BytesIO(imgBytes))
    #
    res = stream_to_multilabel(image_to_stream(img))
    img.show()
    return Response({'closest drug names': res}, status=status.HTTP_200_OK)
