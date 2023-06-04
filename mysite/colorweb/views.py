from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import *
from django.conf import settings
import io
import base64
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FileUploadParser
from .serializers import *
from . import convert_image

# Create your views here.

def register(request):
    form = Registrationform()
    if request.method == 'POST':
        form = Registrationform(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/colorize/')
    return render(request, 'image/register.html', {'form':form})

# convert without login function
def home(request):
    print('in home')
    if request.method == 'POST' and request.FILES['input_image']:
        input_image = request.FILES['input_image']
        fs = FileSystemStorage()
        input_filename = fs.save(input_image.name, input_image)
        input_image_url = fs.url(input_filename)

        output_image = convert_image.convert_image(input_image)
        output_image_bytes = io.BytesIO()
        output_image.save(output_image_bytes, format='JPEG')
        output_image_bytes = output_image_bytes.getvalue()
        output_image_url = f"data:image/jpeg;base64,{base64.b64encode(output_image_bytes).decode()}"

        return render(request, 'image/home.html', {'input_image_url': input_image_url, 'output_image_url':output_image_url})
    return render(request, 'image/home.html')

# convert with login function
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('/result')
    else:
        form = ImageForm()

    # display recent images
    username = request.user.username
    user = User.objects.get(username=username)
    images = BlackWhiteImage.objects.filter(user=user)
    images_count = min(6, images.count())
    input_image_urls = []
    output_image_urls = []
    for image in images[0:images_count]:
        input_image_urls.append(image.bw_img.url)
        output_image_urls.append(image.output_image.url)
        image_pairs = zip(input_image_urls, output_image_urls)

    return render(request, 'image/upload.html', {'form': form, 'image_pairs': image_pairs})

# display result
def display_image(request):
    username = request.user.username
    user = User.objects.get(username=username)
    image = BlackWhiteImage.objects.filter(user=user)[0]

    input_image_url = image.bw_img.url
    output_image = convert_image.convert_image(image.bw_img)
    buffer = io.BytesIO()
    output_image.save(buffer, format='JPEG')
    image.output_image.save(image.bw_img.name,
                            InMemoryUploadedFile(buffer, None, image.bw_img.name, 'image/jpeg', buffer.getbuffer().nbytes, None))
    image.save()
    output_image_url = image.output_image.url
    return render(request, 'image/display.html',
                  {'input_image_url': input_image_url, 'output_image_url': output_image_url})


# class ImageUploadParser(FileUploadParser):
#     media_type = 'image/*'

# class ImageConversionAPI(APIView):
#     parser_classes = [MultiPartParser, ImageUploadParser]
#     # queryset = BlackWhiteImage.objects.all()
#     serializer_class = ImageSerializer
#
#     # def get(self, request, format=None):
#     #     test_image = MyData('test_image', "http://localhost:8000/media/uploads/87086058_113669043545810_6510123926184525824_n.jpg")
#     #     serializer = self.serializer_class(test_image)
#     #     return Response(serializer.data)
#     #
#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)
#         input_image = request.FILES['input_image']
#         # headers = {'Content-Disposition': f'attachment; filename=input.jpg'}
#         if serializer.is_valid():
#             image = serializer.validated_data['image']
#             # serializer.save()
#             # Do something with the image, such as save it to disk
#             # return Response({'message': 'Image uploaded successfully'})
#             return Response(serializer.data, status=200)
#         else:
#             return Response(serializer.errors, status=400)

    # def post(self, request, format=None):
    #     print(request.data)
    #     # input_image = request.FILES['input_image']
    #     serializer = ImageSerializer(data=request.data)
    #     if serializer.is_valid():
    #         # serializer.save()
    #         input_image = serializer.validated_data['image']
    #         # Converting the input image
    #         output_image_bytes = convert_image(input_image)
    #         output_image_url = f"data:image/jpeg;base64,{base64.b64encode(output_image_bytes).decode()}"
    #         # output_image_bytes.seek(0)
    #         # Return the output image as a response
    #         response = Response(ImageSerializer({'image':output_image_url}).data,
    #                             status=status.HTTP_200_OK)
    #         response['Content-Disposition'] = 'attachment; filename=output.jpg'
    #         return response
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
class MyImageAPI(ModelViewSet):
    # parser_classes = [MultiPartParser, ImageUploadParser]
    queryset = BlackWhiteImage.objects.all()
    serializer_class = MyImageSerializer

    # def get(self, request, format=None):
    #     test_image = MyData('test_image', "http://localhost:8000/media/uploads/87086058_113669043545810_6510123926184525824_n.jpg")
    #     serializer = self.serializer_class(test_image)
    #     return Response(serializer.data)
    #
    # def post(self, request, format=None):
    #     serializer = self.serializer_class(data=request.data)
    #     # headers = {'Content-Disposition': f'attachment; filename=input.jpg'}
    #     if serializer.is_valid():
    #         image = serializer.validated_data['image']
    #         # serializer.save()
    #         # Do something with the image, such as save it to disk
    #         # return Response({'message': 'Image uploaded successfully'})
    #         return Response(serializer.data, status=200)
    #     else:
    #         return Response(serializer.errors, status=400)