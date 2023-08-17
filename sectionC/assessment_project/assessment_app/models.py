from django.db import models

# Create your models here.
# The above class represents a User model with username and password fields.
class User(models.Model):
  username = models.CharField(max_length=254, null=False)
  password = models.CharField(max_length=254, null=False)
  
class BlogPost(models.Model):
  title = models.CharField(max_length=254, null=False)
  content = models.CharField(max_length=254, null=False)
  create_at = models.CharField(max_length=254, null=True)
  author = models.ForeignKey(User,on_delete=models.CASCADE, null=True)