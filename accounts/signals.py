from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 
from accounts.models import User, UserProfile

# This func create User profile after creating User using django signals 
@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        # if created is True we create a new object 
        UserProfile.objects.create(user=instance)
    else:
        try:
            # if we edit user or user already exists, we find him and update
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except: 
            # Create the userprofile if not exist, but we created a new one
            UserProfile.objects.create(user=instance)


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass

