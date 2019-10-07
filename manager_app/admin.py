from django.contrib import admin
from .models import Income, Savings, Expenditure, Organisation
# Register your models here.

admin.site.register(Income)
admin.site.register(Savings)
admin.site.register(Expenditure)
admin.site.register(Organisation)
