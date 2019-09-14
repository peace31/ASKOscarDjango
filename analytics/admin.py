from django.contrib import admin

# Register your models here.
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
    'user_id', 'current_user_name', 'current_guide_id', 'current_step_id', 'current_task_id', 'profilerank', 'rank',
    'connected')


admin.site.register(Profile, ProfileAdmin)
