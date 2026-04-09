from django.contrib import admin

from .models import Case, CaseItem

# Register your models here.
admin.site.register(Case)
admin.site.register(CaseItem)