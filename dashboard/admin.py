from django.contrib import admin
from .models import EventType, ExpenseList, ContributionList, MonthlyContribution, ExpenseType, MonthlyExpense, UsefulLink, BannerImage, EventGallary, GallaryUploadImage


# Register your models here.

admin.site.register(EventType)
admin.site.register(UsefulLink)
admin.site.register(ExpenseType)
admin.site.register(BannerImage)
admin.site.register(GallaryUploadImage)


@admin.register(MonthlyContribution)
class MonthlyContributionAdmin(admin.ModelAdmin):
  list_display = ('user', 'contri_title', 'date', 'amount', 'paid')
  ordering = ('user',)
  search_fields = ('user', 'amount')
  list_filter = ('contri_title', 'paid', 'user',)


class MonthlyContributionInline(admin.TabularInline):
  model = MonthlyContribution
  extra = 0
  fields = ('user', 'date', 'amount', 'paid')


@admin.register(ContributionList)
class ContributionListAdmin(admin.ModelAdmin):
  list_display = ('title', 'date')
  list_filter = ('date',)
  inlines = [MonthlyContributionInline]


@admin.register(MonthlyExpense)
class MonthlyExpenseAdmin(admin.ModelAdmin):
  list_display = ('ExpenseTitle', 'date', 'ExpenseCategory', 'EventCategory', 'whos','ExpenseAmount')
  search_fields = ('user', 'EpenseType', 'event')
  list_filter = ('ExpenseCategory', 'EventCategory', 'ExpenseTitle')


class MonthlyExpenseInline(admin.TabularInline):
  model = MonthlyExpense
  extra = 0
  fields = ('date', 'ExpenseCategory', 'EventCategory', 'whos', 'ExpenseAmount')


@admin.register(ExpenseList)
class ExpenseListAdmin(admin.ModelAdmin):
  list_display = ('title', 'date')
  inlines = [MonthlyExpenseInline]


class GallaryImagesInline(admin.TabularInline):
  model = GallaryUploadImage
  extra = 1


@admin.register(EventGallary)
class EventGallaryAdmin(admin.ModelAdmin):
  list_display = ('title', 'date', 'event')
  inlines = [GallaryImagesInline]
