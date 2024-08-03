from rest_framework import serializers
from rest_framework.response import Response
from blog.models import *



class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = '__all__'