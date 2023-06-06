from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from app.models import test
from app.serializers import TestSerializer
from rest_framework.response import Response


# Create your views here.
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
