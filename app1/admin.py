from django.contrib import admin
from .models import EmailSettings

# Register your models here.
#To display it in the form of table in admin/
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display=('email_host',
                  'email_host_user',
                  'email_port',
                  'email_use_tls')