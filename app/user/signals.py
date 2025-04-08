from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from .models import User, UserActivityLog, Address, UserProfile
from django.utils import timezone


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserActivityLog.objects.create(
        user=user,
        action="User logged in",
        timestamp=timezone.now(),
        ip_address=request.META.get('REMOTE_ADDR')
    )



@receiver(post_save, sender=Address)
def log_address_activity(sender, instance, created, **kwargs):
    action = "Address created" if created else "Address updated"
    UserActivityLog.objects.create(
        user=instance.user,
        action=action,
        timestamp=timezone.now()
    )

@receiver(post_save, sender=User)
def log_user_update(sender, instance, created, **kwargs):
    if not created: 
        UserActivityLog.objects.create(
            user=instance,
            action="User profile updated",
            timestamp=timezone.now()
        )

@receiver(post_save, sender=UserProfile)
def log_user_profile_activity(sender, instance, created, **kwargs):
    action = "User profile created" if created else "User profile updated"
    UserActivityLog.objects.create(
            user=instance.user,
            action=action,
            timestamp=timezone.now()
        )

