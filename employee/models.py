from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    desgination=models.CharField(max_length=250,null=True)
    salary=models.FloatField(default=0.0,null=True)


    def __str__(self):
        return (self.user.first_name)

    @receiver(post_save,sender=User)
    def user_is_created(sender,instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)
        else:
            instance.profile.save()


    