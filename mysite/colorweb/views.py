from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import *
from django.conf import settings
import io
import base64
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from . import convert_image

# Create your views here.

def register(request):
    form = Registrationform()
    if request.method == 'POST':
        form = Registrationform(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('/colorize')
    return render(request, 'image/register.html', {'form':form})

# convert without login function
def home(request):
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

class MyImageAPI(ModelViewSet):
    queryset = BlackWhiteImage.objects.all()
    serializer_class = MyImageSerializer
