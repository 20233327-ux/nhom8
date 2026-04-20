from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Document
from .tasks import process_document_ocr

@receiver(post_save, sender=Document)
def trigger_ocr_on_save(sender, instance, created, **kwargs):
    if created and instance.file_attachment:
        try:
            process_document_ocr.delay(instance.id)
        except Exception:
            pass
