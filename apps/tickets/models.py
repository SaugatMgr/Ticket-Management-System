from django.conf import settings
from django.db import models

from utils.models import BaseModel


class MenuLevel1(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuLevel2(BaseModel):
    parent = models.ForeignKey(
        MenuLevel1, on_delete=models.CASCADE, related_name="children"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.parent} > {self.name}"


class MenuLevel3(BaseModel):
    parent = models.ForeignKey(
        MenuLevel2, on_delete=models.CASCADE, related_name="children"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.parent} > {self.name}"


class TicketStatusPriorityCommon(BaseModel):
    name = models.CharField(max_length=50)
    weight = models.IntegerField(default=0)

    class Meta:
        ordering = ["weight"]
        abstract = True

    def __str__(self):
        return self.name


class TicketStatus(TicketStatusPriorityCommon):
    pass


class TicketPriority(TicketStatusPriorityCommon):
    pass


class Ticket(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tickets",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )
    menu = models.ForeignKey(MenuLevel3, on_delete=models.PROTECT)
    status = models.ForeignKey(TicketStatus, on_delete=models.PROTECT)
    priority = models.ForeignKey(TicketPriority, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.title} ({self.status})"
