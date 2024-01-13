from rest_framework.views import APIView
from .serializers import PostDetailSerializers, PostListSerializers, UserSerializers
from .models import Post
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import UserBlock
from .serializers import UserBlockSerializers
from rest_framework.permissions import AllowAny
from .permissions import IsSuperOrOwner
from django.db.models import Q


@api_view(['POST'])
@permission_classes([AllowAny])
def Userview(request):

    try:        
        user_serializers = UserSerializers(data=request.data)
        if user_serializers.is_valid():

            s_username = user_serializers.validated_data.get('username')
            e_mail = user_serializers.validated_data.get('email')
            p_password = user_serializers.validated_data.get('password')
            user = User.objects.create_user(username=s_username, email=e_mail, password=p_password)
            # print(user)
            user.save()
            return Response(data={'message':'user successfully created'}, status=status.HTTP_201_CREATED)
        return Response(data={'message':'invalid data', 'error': user_serializers.errors})
    except Exception as e:
        return Response(data=str(e))


class PostView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperOrOwner]

    def get(self, request, pk=None):

        s_title = request.query_params.get('title')
        s_body = request.query_params.get('body')
        s_author = request.query_params.get('author')
        
        author_name = request.query_params.get('a_name')
        p_title = request.query_params.get('title')

        try:
            
            if author_name or p_title :

                obj = Post.objects.filter(Q(author__username = author_name) | Q(title = p_title))
                serializer = PostDetailSerializers(obj, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)

            if s_title:

                obj = Post.objects.filter(title=s_title)
                serializer = PostDetailSerializers(obj, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)

            if s_body:

                obj = Post.objects.filter(body=s_body)
                serializer = PostDetailSerializers(obj, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
                    
            if s_author:

                obj = Post.objects.filter(author=s_author)
                serializer =  PostDetailSerializers(obj, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
                    

            if pk is not None:
                if  Post.objects.filter(id=pk).exists():

                    obj = Post.objects.get(id=pk)
                    serializer = PostDetailSerializers(obj)
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                
                return Response(data={"message":"id is not valid"})
            
            obj = Post.objects.all()
            serializer =  PostListSerializers(obj, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data=str(e))
        

    def post(self, request):
        try:

            post_serializer = PostListSerializers(data=request.data)
            
            if post_serializer.is_valid():
                # post_serializer.save()

                s_title = post_serializer.validated_data.get('title')
                s_body = post_serializer.validated_data.get('body')
            
                Post.objects.create(author=request.user, title=s_title, body=s_body)
                
                return Response(data={"message": "object is successfully created"}, status=status.HTTP_201_CREATED)
            
            return Response(data={"message": "Invalid data", "error": post_serializer.errors})
        
        except Exception as e:
            return Response(data={"message":str(e)})


    def put(self, request, pk=None):

        try:
            post_serializer = PostListSerializers(data=request.data)

            if post_serializer.is_valid():
                
                if  Post.objects.filter(id=pk).exists:
                    post_fields = Post.objects.get(id=pk)
                    post_fields.title = post_serializer.validated_data.get('title', post_fields.title)
                    post_fields.body = post_serializer.validated_data.get('body', post_fields.body)
                    post_fields.save()
                    return Response(data={'message': 'post is successfully Updated'})
                
                return Response(data={'message': 'Post with given id not found'})
            
            return Response(data={"message": "Invalid data", "error": post_serializer.errors})
        
        except Exception as e:
            return Response(data= {'message':str(e)})
        
    
    def delete(self, request, pk=None):


        try:
            if Post.objects.filter(id=pk).exists():
                post = Post.objects.get(id=pk)
                post.delete()
                return Response(data={'message':'object deleted successfully'}, status=status.HTTP_200_OK)
            return Response(data={'message':'post with given id doesnot exists'})
        except Exception as e:
            return Response(data={'message': str(e)})
        

class UserBlockView(APIView):
    
    def post(self, request):

        try:
            block_user_id = request.query_params.get('user_id')

            if User.objects.filter(id=block_user_id).exists():

                block_user = User.objects.get(id=block_user_id)

                if block_user == request.user:
                    return Response(data={'message':'you can not block yourself'})
                
                if UserBlock.objects.filter(blocker=request.user, block_user = block_user).exists():
                    return Response(data={'message':' You already block user'})
                
                
                UserBlock.objects.create(blocker=request.user, block_user= block_user)

                return Response(data={'message':f"you successfully block {block_user.username}"}, status=status.HTTP_201_CREATED)
            
            return Response(data={'message':'user not found with given id'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(data={'message': str(e)})
        
    
    def delete(self, request):

        try:
            unblock_user_id = request.query_params.get('user_id')

            if User.objects.filter(id=unblock_user_id).exists():

                unblock_user = User.objects.get(id=unblock_user_id)

                if unblock_user == request.user:
                    return Response(data={'message':'You can not unblock yourself'})
                
                unblock_user = UserBlock.objects.filter(blocker=request.user, block_user=unblock_user)
                unblock_user.delete()

                return Response(data={'message':'You successfully unblock the user'}, status=status.HTTP_200_OK)
            
            return Response(data={'message':'user with given not found'})
        
        except Exception as e:
            return Response(data={'message':str(e)})