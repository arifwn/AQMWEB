from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='image/profile/', blank=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


def create_profile_if_not_exist():
    for user in User.objects.all():
        try:
            user.get_profile()
        except:
            Profile.objects.create(user=user)
            print 'profile created for user', user.username
    