from django.contrib import admin
from .models import CustomUser,customrole,Organisation,uploadfile

class CustomAdmin(admin.ModelAdmin):
    list_editable=('is_active',)
    list_display = ('name','email','is_active')
    list_filter = ('role',)
    filter_horizontal = ('role',)

admin.site.register(CustomUser,CustomAdmin)
admin.site.register(customrole) 
admin.site.register(Organisation)
admin.site.register(uploadfile)
 