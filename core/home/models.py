from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class distress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,blank = True, null=True)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    saved = models.BooleanField(default=False)

class ngo(models.Model):
    username = models.ForeignKey(User,on_delete=models.SET_NULL,blank = True, null=True )
    number = models.IntegerField(max_length=100)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    latitude = models.CharField(max_length=100)
    longitude= models.CharField(max_length=100)

class shelters(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)

class conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    time = models.DateTimeField(auto_now_add=True)  # Automatically set to current time when created

    def __str__(self):
        return f"Conversation ({self.user.username if self.user else 'Unknown User'}, {self.post.post}, {self.time})"

class questions(models.Model):
    convo = models.ForeignKey(conversation, on_delete=models.CASCADE, db_index=True, default=1)
    user = models.CharField(max_length=100, default="user")
    question = models.TextField(default="Default question text")
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to current time when created

    def __str__(self):
        return f"Question ({self.user}, {self.created_at})"


