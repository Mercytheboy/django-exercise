from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from . import models
import jwt
from datetime import datetime, timedelta

# Create your views here.


# The Signup class is an API view that handles user signup requests, validates the input data, checks
# if the user already exists, and saves the user if all validations pass.
class Signup(APIView):
    def post(self, request):
        serializer = serializers.UserSerializers(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get("username")

            if models.User.objects.filter(username=username).exists():
                return Response(
                    {"message": "user already exists"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            serializer.save(
                password=make_password(serializer.validated_data.get("password"))
            )
            return Response(
                {"message": "signup successful"}, status=status.HTTP_201_CREATED
            )
        return Response({"error": serializer.errors})


class Login(APIView):
    def post(self, request):
        serializer = serializers.UserSerializers(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")

            try:
                logged_user = models.User.objects.get(username=username)
            except Exception as e:
                return Response(
                    {"message": "invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            password_check = check_password(password, logged_user.password)

            if password_check:
                token = generate_access_token(logged_user)
                response = Response()
                response.set_cookie("access_token", value=token, httponly=True)
                response.data = {"message": "login success", "access_token": token}
                return response
            return Response(
                {"message": "invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response({"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST)


def generate_access_token(user):
    payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(days=5),
        "iat": datetime.utcnow(),
    }
    access_token = jwt.encode(payload, "secret", algorithm="HS256")

    return access_token


class Post(APIView):
    def post(self, request):
        token = request.COOKIES.get("access_token")

        if not token:
            return Response({"message": "unauthenticated"})
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except Exception as e:
            return Response({"error": str(e)})
        serializer = serializers.BlogPostSerializers(data=request.data)
        try:
            logged_user = models.User.objects.get(id=payload["user_id"])
        except Exception as e:
            return Response({"error": str(e)})

        if serializer.is_valid():
            serializer.save(author=logged_user, create_at=datetime.utcnow())
            return Response(
                {"message": "post successfully created", "post_data": serializer.data}
            )
        return Response({"error": "data is not valid"})

    def get(self, request):
        token = request.COOKIES.get("access_token")

        if not token:
            return Response({"message": "unauthenticated"})
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except Exception as e:
            return Response({"error": str(e)})
        serializer = serializers.BlogPostSerializers(data=request.data)

        posts = models.BlogPost.objects.all()
        serializer = serializers.BlogPostSerializers(posts, many=True)
        return Response({"data": serializer.data})

    def put(self, request):
        token = request.COOKIES.get("access_token")

        if not token:
            return Response({"message": "unauthenticated"})
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except Exception as e:
            return Response({"error": str(e)})
        serializer = serializers.BlogPostSerializers(data=request.data)
        try:
            logged_user = models.User.objects.get(id=payload["user_id"])
        except Exception as e:
            return Response({"error": str(e)})

    def put(self, request):
        token = request.COOKIES.get("access_token")

        if not token:
            return Response(
                {"message": "unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except Exception as e:
            return Response({"error": str(e)})

        post_id = request.data.get("post_id")
        try:
            logged_user = models.User.objects.get(id=payload["user_id"])
            post_to_update = models.BlogPost.objects.get(id=post_id)
        except Exception as e:
            return Response(
                {"error": "post does not exist or may have been deleted"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if post_to_update.author.id != logged_user.id:
            return Response(
                {"message": "Only the creator can update the post"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = serializers.BlogPostSerializers(
            instance=post_to_update, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Post has been updated", "updated post": serializer.data}
            )
        return Response(
            {"error": "Data is not valid"}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request):
        token = request.COOKIES.get("access_token")

        if not token:
            return Response({"message": "unauthenticated"})
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except Exception as e:
            return Response({"error": str(e)})
        try:
            logged_user = models.User.objects.get(id=payload["user_id"])
        except Exception as e:
            return Response({"error": str(e)})

        post_id = request.query_params.get("post_id")
        post_to_delete = models.BlogPost.objects.get(id=post_id)
        if post_to_delete.author.id == logged_user.id:
            post_to_delete.delete()
            return Response(
                {"message": "post has been deleted"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "only creator can delete this post"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
