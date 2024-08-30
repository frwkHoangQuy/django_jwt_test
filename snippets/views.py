from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Middleware.jwt_middleware import PermissionRequiredMixin
from .models import Snippet
from .serializers import SnippetSerializer


class SnippetView(PermissionRequiredMixin, APIView):
    def get(self, request):
        data = []
        for snippet in Snippet.objects.all():
            temp = {}
            temp["id"] = snippet.id
            temp["title"] = snippet.title
            temp["code"] = snippet.code
            temp["linenos"] = snippet.linenos
            temp["language"] = snippet.language
            temp["style"] = snippet.style
            data.append(temp)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        new_item = Snippet(
            title=request.data["title"],
            code=request.data["code"],
            linenos=request.data["linenos"],
            language=request.data["language"],
            style=request.data["style"],
        )
        new_item.save()
        return Response("OK", status=status.HTTP_200_OK)

    def patch(self, request, id):
        new_item = get_object_or_404(Snippet, id=id)
        new_item.title = request.data["title"]
        new_item.code = request.data["code"]
        new_item.linenos = request.data["linenos"]
        new_item.language = request.data["language"]
        new_item.style = request.data["style"]
        new_item.save()
        return Response("OK", status=status.HTTP_200_OK)

    def delete(self, request, id):
        delete_item = get_object_or_404(Snippet, id=id)
        delete_item.delete()
        return Response("OK", status=status.HTTP_200_OK)


class SnippetViewV2(PermissionRequiredMixin, APIView):
    def get(self, request):
        queryset = Snippet.objects.all()
        serializer = SnippetSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializers = SnippetSerializer(data=data,
                                        context={'request': request})
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
