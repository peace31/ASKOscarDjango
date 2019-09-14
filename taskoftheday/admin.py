from django.contrib import admin

# Register your models here.
from .models import Guide, Step, Task, UserTaskHistory


class StepInline(admin.TabularInline):
    model = Step
    extra = 1


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


class GuideAdmin(admin.ModelAdmin):
    inlines = [
        StepInline,
    ]

    list_display = ('name', 'guide_category', 'is_complete')


admin.site.register(Guide, GuideAdmin)


class StepAdmin(admin.ModelAdmin):
    inlines = [
        TaskInline,
    ]

    list_display = ('guide', 'sequence_number', 'name', 'is_complete')


admin.site.register(Step, StepAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'step', 'sequence_number', 'name', 'task_task', 'is_complete')


admin.site.register(Task, TaskAdmin)


class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'guide', 'step', 'task', 'completion_datetime', 'is_complete')


admin.site.register(UserTaskHistory, TaskHistoryAdmin)
