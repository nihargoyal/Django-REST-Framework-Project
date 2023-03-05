#from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ToDo
from .serializers import TodoSerializer

# Create your views here.

class TodoListApiView(APIView):

    def get(self, request, *args, **kwargs):
        todo=ToDo.objects.all()
        serializers=TodoSerializer(todo, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data=request.data
        serializer= TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailApiView(APIView):

    def get_object(self, todo_id, *args, **kwargs):
        try:
            return ToDo.objects.get(id=todo_id)
        except ToDo.DoesNotExist:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, todo_id, *args, **kwargs):
        todo_instance=self.get_object(todo_id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer=TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )
        data = request.data
        serializer = TodoSerializer(instance = todo_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(todo_id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_404_NOT_FOUND
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_100_CONTINUE
        )