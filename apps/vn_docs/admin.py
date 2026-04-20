from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('doc_number', 'title', 'doc_type', 'status', 'date_issued')
    list_filter = ('doc_type', 'status', 'date_issued')
    search_fields = ('doc_number', 'title', 'sender_org', 'receiver_org')
    date_hierarchy = 'date_issued'
    readonly_fields = ('date_created', 'content_extracted')
from django.contrib import admin

# Register your models here.
