from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from main.models import Products6,Order,UserProfile,multimage,Category6
# Register your models here.

class CustomMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 10

admin.site.register(Category6,CustomMPTTModelAdmin)

admin.site.register(multimage)



admin.site.register(Products6)

admin.site.register(Order)

admin.site.register(UserProfile)

