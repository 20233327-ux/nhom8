from django.apps import AppConfig


class VnDocsConfig(AppConfig):
    name = 'vn_docs'

    def ready(self):
        import vn_docs.signals

