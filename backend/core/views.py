
##Forma mas basica de crear un API
from rest_framework.views import APIView
from rest_framework.response import Response

class TestView(APIView):
    def get(self,request,*args, **kwargs):
        return Response("Hola Mundo")