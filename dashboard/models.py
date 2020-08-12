from django.db import models
from datetime import date
from simple_history.models import HistoricalRecords
from account.models import TeamMember
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class EventType(models.Model):
  title = models.CharField('Event type name', max_length=100)

  def __str__(self):
    return self.title


class ExpenseType(models.Model):
  title = models.CharField('Expense type name', max_length=100)

  def __str__(self):
    return self.title


class ExpenseList(models.Model):
  title = models.CharField(max_length=100)
  date = models.DateField()

  def __str__(self):
    return self.title


class MonthlyExpense(models.Model):
  ExpenseTitle = models.ForeignKey(ExpenseList, null=True, blank=True, on_delete=models.SET_NULL)
  date = models.DateField(null=True, blank=True)
  ExpenseCategory = models.ForeignKey(ExpenseType, null=True, blank=True, on_delete=models.SET_NULL)
  EventCategory = models.ForeignKey(EventType, null=True, blank=True, on_delete=models.SET_NULL)
  whos = models.ForeignKey(TeamMember, null=True, blank=True, on_delete=models.SET_NULL)
  ExpenseAmount = models.IntegerField('Expense Amount', default=100)


class ContributionList(models.Model):
  title = models.CharField(max_length=100)
  date = models.DateField()

  def __str__(self):
    return self.title


class MonthlyContribution(models.Model):
  contri_title = models.ForeignKey(ContributionList, null=True, blank=True, on_delete=models.SET_NULL)
  user = models.ForeignKey(TeamMember, null=True, blank=True, on_delete=models.SET_NULL)
  date = models.DateField(null=True, blank=True)
  amount = models.IntegerField(default=100)
  paid = models.BooleanField()

  def __str__(self):
    strings = str(self.contri_title) + ' | ' + str(self.user)
    return strings


#This will create all member entry instance automatically for MonthlyContribution
#when you add new entry in ContributionList.
@receiver(post_save, sender=ContributionList)
def create_monthly_contri_instance_for_all_user(sender, created, instance, **kwargs):
  if created:
    team_data = TeamMember.objects.values().filter(status=1)
    for member in team_data:
      monthly_contri_per_usr = MonthlyContribution(contri_title=instance, user_id=member['id'], paid=False)
      monthly_contri_per_usr.save()


class UsefulLink(models.Model):
  title = models.CharField(max_length=200)
  link = models.CharField(max_length=500)

  def __str__(self):
    return self.title


class BannerImage(models.Model):
  years =  tuple([(r,r) for r in range(2018, date.today().year+1)])
  title = models.CharField(max_length=200)
  year = models.IntegerField(choices = years)
  image = models.ImageField(upload_to="gallery/banner")
  description = models.CharField(max_length=30)

  def __str__(self):
    return self.title

class EventGallary(models.Model):
  title = models.CharField(max_length=200)
  date = models.DateField()
  event = models.ForeignKey(EventType, null=True, blank=True, on_delete=models.SET_NULL)

  def __str__(self):
    return "{}-{}".format(self.title, self.date.strftime("%b-%Y"))

def image_directory_path(instance, filename):
  today = date.today()
  return 'gallery/event/{0}/{1}/{2}'.format(today.year, instance.title, filename)


class GallaryUploadImage(models.Model):
  title = models.ForeignKey(EventGallary, null=True, blank=True, on_delete=models.SET_NULL)
  image = models.ImageField(upload_to=image_directory_path)
