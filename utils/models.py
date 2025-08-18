import uuid

from django.conf import settings
from django.db import models

from utils.threads import get_current_user


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_created",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_modified",
    )
    created_at = models.DateTimeField("created at", auto_now_add=True)
    modified_at = models.DateTimeField("last modified at", auto_now=True)

    def save(self, *args, **kwargs):
        from apps.users.models import CustomUser

        user = get_current_user()

        if isinstance(user, CustomUser):
            if not self.pk:
                self.created_by = user
            self.modified_by = user
        else:
            self.created_by = None
            self.modified_by = None

        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
