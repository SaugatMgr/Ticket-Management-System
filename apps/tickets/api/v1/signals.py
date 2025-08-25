from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notifications.models import NotificationLog
from apps.tickets.models import Ticket
from utils.constants import NotificationLogActionChoices


@receiver(post_save, sender=Ticket)
def ticket_notifications(sender, instance, created, **kwargs):
    content_type = ContentType.objects.get_for_model(Ticket)

    if created:
        NotificationLog.objects.create(
            user=instance.created_by,
            action=NotificationLogActionChoices.CREATE,
            content_type=content_type,
            object_id=instance.id,
            message=f"Ticket {instance.id} created by {instance.created_by}",
        )
        print("**********Ticket Created**********")
        print(f"Notification: Ticket {instance.id} created")
        print("**********Ticket Created**********")

    else:
        NotificationLog.objects.create(
            user=instance.modified_by,
            action=NotificationLogActionChoices.UPDATE,
            content_type=content_type,
            object_id=instance.id,
            message=f"Ticket {instance.id} updated by {instance.modified_by}",
        )
        print("**********Ticket Updated**********")
        print(f"Notification: Ticket {instance.id} updated")
        print("**********Ticket Updated**********")
