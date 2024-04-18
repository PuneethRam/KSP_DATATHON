from django.db import models

# Create your models here.

class AnalysisResult(models.Model):
    name = models.CharField(max_length=100)
    video_url = models.URLField()
    channel_name=models.CharField(null=True,max_length=100)
    description_score = models.FloatField(null=True, blank=True)
    about_score = models.FloatField(null=True, blank=True)
    promotion = models.CharField(max_length=255, null=True, blank=True)
    transcript_score = models.FloatField(null=True, blank=True)
    comments_score = models.FloatField(null=True, blank=True)
    overall_score = models.FloatField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    video_report = models.CharField(max_length=1000, null=True, blank=True)
    overall_report = models.CharField(max_length=1000, null=True, blank=True)
    conclusion = models.CharField(max_length=255, null=True, blank=True)

class TelegramAnalysis(models.Model):
    name = models.CharField(max_length=100)
    channel_name= models.CharField(max_length=100)
    channel_report = models.CharField(max_length=1000, null=True, blank=True)
    channel_score = models.FloatField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    conclusion = models.CharField(max_length=255, null=True, blank=True)

class Product(models.Model):
    id    = models.AutoField(primary_key=True)
    name  = models.CharField(max_length = 100) 
    info  = models.CharField(max_length = 100, default = '')
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
