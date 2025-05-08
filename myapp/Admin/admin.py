from django.contrib import admin
from . models import user_details,Course,Module,UserProgress
admin.site.register(user_details)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(UserProgress)