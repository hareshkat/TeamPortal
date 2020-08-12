from django.contrib import admin
from .models import IsrTracking, IsrTaskList, IsrUsefulDocument
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
# @admin.register(IsrUsefulDocument)
class IsrTaskListAdmin(admin.ModelAdmin):
  list_display = ('title', 'Documents')


class ISRDocumentInline(admin.TabularInline):
  model = IsrUsefulDocument
  extra = 1
  field = ('Documents')


# @admin.register(IsrTaskList)
class IsrTaskListAdmin(admin.ModelAdmin):
  list_display = ('IsrNumber', 'TaskId', 'TaskCategory', 'TaskStatus', 'TaskAssignee', 'TargetClosureDate')
  list_filter = ('TaskCategory', 'TaskStatus', 'TargetClosureDate')


class ISRTaskInline(admin.TabularInline):
  model = IsrTaskList
  extra = 1
  fields = ('TaskId', 'TaskCategory', 'TaskStatus', 'TaskAssignee', 'TargetClosureDate')


@admin.register(IsrTracking)
class IsrTrackingHistoryAdmin(SimpleHistoryAdmin):
  list_display = ('IsrNumber', 'RequestCategory', 'IsrStatus', 'LmsInstance', 'SevirityLevel', 'Description', 'assignees', 'RequestDate')
  search_fields = ('IsrNumber', 'Description', 'FeatureDefectNumber')
  list_filter = ('RequestCategory', 'IsrStatus', 'LmsInstance', 'SevirityLevel', 'RequestDate', 'Assignee')
  filter_horizontal = ['Assignee']
  inlines = [ISRTaskInline, ISRDocumentInline]
  history_list_display = ['IsrStatus']
  fieldsets = (
                (None, {'fields': (('IsrNumber', 'RequestCategory', 'IsrStatus'),
                  ('LmsInstance', 'FindingEnv', 'SevirityLevel'),
                  ('Description','FeatureDefectNumber'),
                  ('RequestDate', 'ClosingDate'),
                  ('Assignee'),
                  )}),
            )
