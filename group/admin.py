from django.contrib import admin
from group.models import *

# Register your models here.
admin.site.register(Group)
admin.site.register(Questions)
admin.site.register(Members)
admin.site.register(Ratings)
admin.site.register(GroupQn)
admin.site.register(Suggested_members)
admin.site.register(Suggested_questions)