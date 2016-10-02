from django.contrib import admin
from .models import Donation

# Register your models here.

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
