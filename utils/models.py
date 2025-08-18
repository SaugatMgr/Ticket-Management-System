import uuid

from django.contrib.auth import get_user_model
from django.db import models

from utils.threads import get_current_user

User = get_user_model()


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_created",
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_modified",
    )
    created_at = models.DateTimeField("created at", auto_now_add=True)
    modified_at = models.DateTimeField("last modified at", auto_now=True)

    def save(self, *args, **kwargs):
        user = get_current_user()

        if isinstance(user, User):
            if not self.pk and not self.created_by:
                self.created_by = user
            self.modified_by = user
        else:
            self.created_by = None
            self.modified_by = None

        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
