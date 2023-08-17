# section B

# Number 1
"""
--> the null key values of the title and author is automatically set to true. would allow the user to populate the database with empty data
"""

# answer
"""
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length = 200, null =True)
    author = models.CharField(max_length = 200, null =True)
    publication_year = models.PositiveIntegerField()
"""

# number 2
"""
--> import error on line 1. The appropriate import code is 'from rest_framework...' not '. from rest_framework...'
--> import error on line 2. since the models.py file is on the same file level as the serializer.py file, the code 'from . models import models' would throw an error
--> serializer should be linked with the model
"""


# answer
"""
from rest_framework import serializers
from . import models

class BookSerializers(serializers.Serializer):
    class Meta:
        model = models.Book
        fields =('id', 'title', 'author', 'publication_year')
        read_only_fields = ('id',)
"""

# Number 3: what is the use case of loops?

'''
--> loops are used to execute a sequence of codes repeatedly as long as the defined condition is true. When the condition becomes false, it breaks.
'''

# What is the use case of conditional statement?
'''
--> conditional statements set a condition for a code to be executed. 
'''