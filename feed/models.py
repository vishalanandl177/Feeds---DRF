from django.db import models
from django.utils import timezone
from rest_framework.reverse import reverse
from user.models import User


class Feed(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(db_index=True, max_length=150)
    description = models.TextField()
    tags = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='feeds/%s-%s/' % (timezone.now().month, timezone.now().year), null=True)
    likes = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)

    # Auto add timestamp when created
    added_on = models.DateTimeField(null=True, auto_now_add=True)

    # Always update timestamp when updated
    updated_on = models.DateTimeField(null=True, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_instance(self):
        return self

    def get_absolute_url(self):
        return reverse('feed:feeds', args=[self.id])

    class Meta:
        ordering = ('-added_on',)
        verbose_name = 'Feed'
        verbose_name_plural = 'Feeds'


class FavouriteFeed(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    feed = models.ForeignKey(Feed, on_delete=models.DO_NOTHING)

    # Auto add timestamp when created
    added_on = models.DateTimeField(null=True, auto_now_add=True)

    # Always update timestamp when updated
    updated_on = models.DateTimeField(null=True, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def get_instance(self):
        return self

    class Meta:
        ordering = ('-added_on',)
        verbose_name = 'Favourite feed'
        verbose_name_plural = 'Favourite feeds'


class LikedFeed(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    feed = models.ForeignKey(Feed, on_delete=models.DO_NOTHING)

    # Auto add timestamp when created
    added_on = models.DateTimeField(null=True, auto_now_add=True)

    # Always update timestamp when updated
    updated_on = models.DateTimeField(null=True, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def get_instance(self):
        return self

    class Meta:
        ordering = ('-added_on',)
        verbose_name = 'Liked Feed'
        verbose_name_plural = 'Liked Feeds'
