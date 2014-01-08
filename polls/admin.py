from django.contrib import admin
from polls.models import Poll, Choice

# Register your models here.
class ChoiseInline(admin.TabularInline):
    model = Choice
    extra = 3
class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['question']}),
        ('Date published', {'fields':['pub_date']}),
    ]
    inlines = [ChoiseInline]

admin.site.register(Poll,PollAdmin)
