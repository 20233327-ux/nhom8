from django.apps import AppConfig


class VnDocsConfig(AppConfig):
    name = 'vn_docs'

    def ready(self):
        # Signals temporarily disabled - pdfplumber not installed
        pass
        # import vn_docs.signals

