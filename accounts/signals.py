from django.db.models.signals import post_save
from .models import User, UserProfile
from django.dispatch import receiver

# @receiver(post_save, sender=User) -- Another way of calling django signal 
def postsave_add_UserProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user= instance)
    else:
        try:
            profile= UserProfile.objects.get(user= instance)
            profile.save()
        except:
            UserProfile.objects.create(user= instance)

post_save.connect(postsave_add_UserProfile, sender= User)