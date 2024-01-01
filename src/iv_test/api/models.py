from django.db import models

# Create your models here.


class AiAnalysisLog(models.Model):
    image_path = models.CharField(max_length=255)
    success = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    class_id = models.IntegerField(db_column='class')
    confidence = models.DecimalField(max_digits=5, decimal_places=4)
    request_timestamp = models.PositiveIntegerField()
    response_timestamp = models.PositiveIntegerField()

    class Meta:
        db_table = 'ai_analysis_log'
