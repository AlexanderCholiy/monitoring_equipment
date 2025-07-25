from django.contrib import admin

from .constants import MAX_SUBSCRIBER_PER_PAGE
from .forms import SubscriberForm
from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('imsi', 'subscriber_status', 'operator_determined_barring')
    list_per_page = MAX_SUBSCRIBER_PER_PAGE
    search_fields = ('imsi',)
    list_filter = ('subscriber_status', 'operator_determined_barring',)
    ordering = ('-pk',)
    list_editable = ('subscriber_status', 'operator_determined_barring')
    form = SubscriberForm

    fieldsets = (
        ('Subscriber Configuration', {
            'fields': (
                'imsi',
                'msisdn',
                'security',
                'ambr',
                'subscriber_status',
                'operator_determined_barring',
            )
        }),
        ('Slice Configurations', {
            'fields': ('slice',)
        }),
    )

    class Media:
        js = ('js/subscriber_form/unit_mapping_admin.js',)
