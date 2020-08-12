from django.contrib import admin
from .models import TeamMember

# Register your models here.
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
  list_display = ('name', 'emp_id', 'email', 'status')
  ordering = ('name',)
  search_fields = ('name', 'emp_id')
  list_filter = ('status',)
