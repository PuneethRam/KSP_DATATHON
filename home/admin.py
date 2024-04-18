from django.contrib import admin

from django.apps import apps
from .models import AnalysisResult
from .models import TelegramAnalysis

# Register your models here.
admin.site.register(AnalysisResult)
admin.site.register(TelegramAnalysis)

app_models = apps.get_app_config('home').get_models()
for model in app_models:
    try:    

        admin.site.register(model)

    except Exception:
        pass
