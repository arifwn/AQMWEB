from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User)
    
    # -- OAuth 1.0 services --
    # Twitter: https://dev.twitter.com/docs/auth/implementing-sign-twitter
    twitter_oauth_token = models.TextField(blank=True)
    twitter_oauth_secret = models.TextField(blank=True)
    
    # LinkedIn: http://developer.linkedin.com/documents/linkedins-oauth-details
    linkedin_oauth_token = models.TextField(blank=True)
    linkedin_oauth_secret = models.TextField(blank=True)
    
    # Yahoo: http://developer.yahoo.com/oauth/guide/index.html
    yahoo_oauth_token = models.TextField(blank=True)
    yahoo_oauth_secret = models.TextField(blank=True)
    
    # -- OAuth 2.0 services --
    # Facebook: https://developers.facebook.com/docs/authentication/
    facebook_access_token = models.TextField(blank=True)
    
    # Google: http://code.google.com/apis/accounts/docs/OAuth2WebServer.html
    google_access_token = models.TextField(blank=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
