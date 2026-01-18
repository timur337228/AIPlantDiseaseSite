from django.db import models
from django.conf import settings

class PlantInfo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="plant_models",
        null=True,
    )
    image = models.ImageField(upload_to='plant_images/', blank=True, null=True)
    prediction = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    