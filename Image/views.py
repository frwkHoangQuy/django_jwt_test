from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import ImageSerializer


class ImageView(APIView):
    def post(self, request):
        print(request.data)
        return Response(1, status=status.HTTP_200_OK)


class ImageViewSet(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file = request.data.get('image')
        if not file:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
