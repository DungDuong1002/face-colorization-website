from rest_framework import serializers
from .views import BlackWhiteImage

class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField(allow_null=False)

class MyDataSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    image = serializers.ImageField()

class MyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlackWhiteImage
        fields = ['bw_img', 'user', 'date', 'output_image']