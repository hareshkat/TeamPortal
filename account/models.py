from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class TeamMember(models.Model):
  GENDER = (('M', 'Male'),('F', 'Female'),)
  user_status = ((1, 'Active'),(0, 'In-Active'))

  name = models.OneToOneField(User, on_delete=models.CASCADE)
  emp_id = models.CharField(max_length=12)
  email = models.EmailField(max_length = 200)
  contact_no = models.CharField(max_length=12)
  dob = models.DateField(null=True)
  gender = models.CharField(max_length=1, choices=GENDER)
  status = models.IntegerField(default = 1, choices=user_status)
  about_me = models.CharField(max_length=200, null=True, blank=True)

  class Meta:
    ordering = ('name', 'dob')

  def __str__(self):
    return str(self.name)


#This will create new member instance automatically when you add new user in django site
@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, created, instance, **kwargs):
  if created:
    profile = TeamMember(name=instance)
    profile.save()
