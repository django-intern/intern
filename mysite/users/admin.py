from django.contrib import admin
from .models import Task, Account, Notice, Comment

admin.site.register(Task)
admin.site.register(Account)
admin.site.register(Notice)
admin.site.register(Comment)