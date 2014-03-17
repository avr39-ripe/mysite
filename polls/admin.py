from django.contrib import admin
from polls.models import Poll, Choice

# Register your models here.


class ChoiseInline(admin.TabularInline):
    model = Choice
    extra = 3


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question']}),
        ('Date published', {'fields': ['pub_date']}),
    ]
    list_display = ['question', 'pub_date', 'was_published_recently']
    inlines = [ChoiseInline]
    list_filter = ['pub_date']
    search_fields = ['question']

admin.site.register(Poll, PollAdmin)
