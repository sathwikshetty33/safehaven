from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}"
@receiver(post_save, sender=ChatMessage)
def send_message_notification(sender, instance, created, **kwargs):
    if created:
        # Fetch all user emails
        recipients = User.objects.exclude(email="").values_list('email', flat=True)

        # Prepare the email
        subject = f"New Message from {instance.user.username}"
        message = f"{instance.user.username} says:\n\n{instance.message}"
        from_email = "your_email@example.com"

        # Send the email to all users
        send_mail(
            subject,
            message,
            from_email,
            list(recipients),
            fail_silently=False,
        )
        print("message sent")