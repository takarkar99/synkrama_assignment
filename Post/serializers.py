from rest_framework import serializers
from .models import Post, UserBlock
from django.contrib.auth.models import User


class UserSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username','email']


class PostListSerializers(serializers.ModelSerializer):

    # author = UserSerializers(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body']


class PostDetailSerializers(serializers.ModelSerializer):

    author_username = serializers.CharField(source='author.username', read_only=True)
    author_email = serializers.EmailField(source='author.email', read_only=True)
    

    class Meta:

        model = Post
        fields = ['id','title', 'body', 'author_username', 'author_email']


class UserBlockSerializers(serializers.ModelSerializer):

    block_user = serializers.ModelSerializer(read_only=True)

    class Meta:
        model = UserBlock
        fields = '__all__'