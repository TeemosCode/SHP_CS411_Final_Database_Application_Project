from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import Blogpost, Buser
from .api.serializers import BlogPostSerializer, BusersSerializer
# Create your views here.


@csrf_exempt
def post_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Blogpost.objects.all()
        serializer = BlogPostSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     serializer = Blogpost(data=data)
    #     try:
    #         serializer.save()
    #     except:
    #         return JsonResponse(serializer.data, status=201)
    #     return JsonResponse(serializer.errors, status=400)

