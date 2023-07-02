from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Cart

@receiver(post_save,sender=User)
def build(sender,instance,created,**kwargs):
    if created:
        cart=Cart.objects.create(user=instance)
@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.cart.save()