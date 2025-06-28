from django.contrib import admin
from .models import Worker, CheckIn


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'first_name', 'last_name')
    search_fields = ('telegram_id', 'username', 'first_name', 'last_name')
    ordering = ('last_name', 'first_name')
    readonly_fields = ('telegram_id',)


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('worker', 'check_in_time', 'location_name')
    list_filter = ('check_in_time',)
    search_fields = ('worker__username', 'worker__first_name', 'location_name')
    readonly_fields = ('check_in_time',)
    date_hierarchy = 'check_in_time'
    raw_id_fields = ('worker',)
