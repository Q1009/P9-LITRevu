import os
import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


def ticket_image_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'{uuid.uuid4().hex}{ext}'


class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=8192, verbose_name="Description")
    image = models.ImageField(upload_to=ticket_image_path, verbose_name="Image", max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Auteur")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_edited = models.DateTimeField(auto_now=False, null=True, blank=True, verbose_name="Date de modification")


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, verbose_name="Ticket")
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Note")
    headline = models.CharField(max_length=128, verbose_name="Titre")
    body = models.TextField(max_length=8192, blank=True, verbose_name="Commentaire")
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Auteur")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")


class UserFollows(models.Model):
    # Your UserFollows model definition goes here
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follows')
    user_followed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'user_followed')