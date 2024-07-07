from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class User(AbstractUser):
    username = models.CharField(unique=True, max_length=120)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=120, blank=True)
    otp = models.CharField(max_length=120, unique=True,null= True, blank= True)
    refresh_token = models.CharField(max_length=120, unique=True,null= True, blank= True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.full_name:
            email_username, _ = self.email.split("@")
            self.full_name = email_username
        super(User, self).save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user_folder", default="default-user.jpg", null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True)
    about = models.TextField(max_length=120, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name if self.user.full_name else str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)