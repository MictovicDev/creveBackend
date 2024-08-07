from rest_framework import serializers
from rest_framework.response import Response
from blog.models import *




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()


    class Meta:
        model = Blog
        fields = '__all__'

    def get_category(self, obj):
        return CategorySerializer(obj.category).data