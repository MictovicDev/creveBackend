from django.shortcuts import render
from rest_framework import generics,permissions,status, response
from blog.serializers import BlogSerializer
from .models import Blog

# Create your views here.





class BlogView(generics.ListAPIView):
    queryset = Blog.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlogSerializer
    