from rest_framework import serializers
from . import models

# The class `UserSerializers` is a serializer class for the `User` model with fields for `id`,
# `username`, and `password`, and the `id` field is read-only.
class UserSerializers(serializers.ModelSerializer):
  class Meta:
    model = models.User
    fields= ('id','username', 'password')
    read_only_fields = ('id',)
    
# The above class is a serializer for the BlogPost model in Python, which includes fields for id,
# title, content, create_at, and author, with the id field set as read-only.
class BlogPostSerializers(serializers.ModelSerializer):
  class Meta:
    model = models.BlogPost
    fields= ('id','title', 'content', 'create_at', 'author')
    read_only_fields = ('id',)


    