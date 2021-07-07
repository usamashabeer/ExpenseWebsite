from django.contrib import admin
from .models import Expense, Category


# Register your models here.

# admin.site.register(Expense)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['owner', 'category']


admin.site.register(Category)
