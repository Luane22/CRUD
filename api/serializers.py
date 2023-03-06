from rest_framework import serializers
from .models import MyModel
from rest_framework import generics
from .serializers import MyModelSerializer

class MyModelList(generics.ListCreateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
