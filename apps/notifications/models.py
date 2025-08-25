from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from utils.constants import NotificationLogActionChoices
from utils.models import BaseModel

User = get_user_model()


# Create your models here.
class NotificationLog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(
        max_length=20, choices=NotificationLogActionChoices.choices
    )
    message = models.TextField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.user} {self.action} {self.content_type} ({self.object_id})"

    class Meta:
        verbose_name = "Notification Log"
        verbose_name_plural = "Notification Logs"
