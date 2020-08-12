from django.db import models
from simple_history.models import HistoricalRecords
from account.models import TeamMember

# Create your models here.
class IsrTracking(models.Model):
  isr_status = (('open', 'Open'), ('wip', 'Work In Progress'), ('closed', 'Closed'), ('discard','Discard'))
  request_category = (('assessment', 'Assessment'), ('finding', 'Finding'), ('exception', 'Exception'))
  lms_category = (('emp_lms', 'Employee LMS'), ('partner_lms', 'Partner LMS'), ('tech_lms', 'Tech LMS'))
  env_choice = (('sit', 'SIT'), ('replica', 'Replica'), ('production', 'Production'))
  sevirity_choice = (('low', 'Low(1)'), ('medium', 'Medium(2)'), ('high', 'High(3)'))

  IsrNumber = models.CharField('ISR Number', unique=True, max_length=20)
  RequestCategory = models.CharField('Request Category', choices=request_category, max_length=20)
  IsrStatus = models.CharField('ISR Status', choices=isr_status, max_length=20)
  Description = models.CharField('Description', max_length = 500, blank=True)
  LmsInstance = models.CharField('LMS Instance', choices=lms_category, max_length=20, blank=True)
  FindingEnv = models.CharField('Finding Environment', choices=env_choice, max_length=20, blank=True)
  SevirityLevel = models.CharField('Sevirity Level', choices=sevirity_choice, max_length=20, blank=True)
  Assignee = models.ManyToManyField(TeamMember, blank=True)
  RequestDate = models.DateField('Request Date', null=True, blank=True)
  ClosingDate = models.DateField('Closing Date', null=True, blank=True)
  FeatureDefectNumber = models.CharField('Feature/Defect Number', max_length=20, null=True, blank=True)
  history = HistoricalRecords()

  class Meta:
    verbose_name = "ISR"
    verbose_name_plural = "ISR"

  def assignees(self):
    return ", ".join([str(p.name) for p in self.Assignee.all()])

  def __str__(self):
    return str(self.IsrNumber)


class IsrTaskList(models.Model):
  task_category_options = (('app_sec_assessment', 'App. Security Assessment'),
                ('eqxe_request', 'Exception Request'),
                ('privacy_assessment', 'Privacy Assessment (App/Device)'),
                ('infra_assessment', 'Infrastructure Assessment'), ('other', 'Other'))
  task_status_options = (('open', 'Open'), ('closed', 'Closed'), ('discard','Discard'))

  IsrNumber = models.ForeignKey(IsrTracking, null=True, blank=True, on_delete=models.SET_NULL)
  TaskId = models.CharField('Task Id', unique=True, max_length=20, blank=True)
  TaskCategory = models.CharField('Task Category', choices=task_category_options, max_length=50, blank=True)
  TaskStatus = models.CharField('Task Status', choices=task_status_options, max_length=50, blank=True)
  TaskAssignee = models.CharField('Task Spoc person/Team', max_length=100, blank=True)
  TargetClosureDate = models.DateField('Task Closure Date', null=True, blank=True)

  class Meta:
    verbose_name = "ISR - Task"
    verbose_name_plural = "ISR - Tasks"

  def __str__(self):
    return str(self.IsrNumber)


def isr_doc_directory_path(instance, filename):
  return 'InfoSec/{0}/{1}'.format(instance.title, filename)


class IsrUsefulDocument(models.Model):
  title = models.ForeignKey(IsrTracking, null=True, blank=True, on_delete=models.SET_NULL)
  Documents = models.FileField('Attachments/Supporting Documents', upload_to=isr_doc_directory_path, blank=True)

  def __str__(self):
    return str(self.title)
