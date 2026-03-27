import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Ticket


@receiver(post_delete, sender=Ticket)
def delete_ticket_image(sender, instance, **kwargs):
    if instance.image:
        print(
            f"Deleting image for ticket {instance.id}: {instance.image.path}")
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Ticket)
def delete_old_ticket_image(sender, instance, **kwargs):
    try:
        old_ticket = Ticket.objects.get(pk=instance.pk)
    except Ticket.DoesNotExist:
        return False

    old_image = old_ticket.image
    new_image = instance.image

    if not old_image == new_image:
        print(f"Deleting old image for ticket {instance.id}: {old_image.path}")
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
