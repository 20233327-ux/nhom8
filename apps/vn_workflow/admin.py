from django.contrib import admin
from .models import WorkflowDefinition, WorkflowStep, DocumentWorkflow, ApprovalHistory

class WorkflowStepInline(admin.TabularInline):
    model = WorkflowStep
    extra = 1

@admin.register(WorkflowDefinition)
class WorkflowDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    inlines = [WorkflowStepInline]

@admin.register(DocumentWorkflow)
class DocumentWorkflowAdmin(admin.ModelAdmin):
    list_display = ('document', 'workflow', 'current_step', 'status')
    list_filter = ('status', 'workflow')

@admin.register(ApprovalHistory)
class ApprovalHistoryAdmin(admin.ModelAdmin):
    list_display = ('doc_workflow', 'step', 'approver', 'action', 'timestamp')
    readonly_fields = ('timestamp',)
