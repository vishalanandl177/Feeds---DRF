from django.contrib import admin
from django.utils.safestring import mark_safe
from . import models


class FeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'picture', 'added_on')
    search_fields = ('title',)
    readonly_fields = ('picture',)

    def picture(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=50,
            height=50,
        )
        )


class LikedFeedAdmin(admin.ModelAdmin):
    list_display = ('user', 'added_on', 'is_deleted')
    search_fields = ('user',)
    list_filter = ('is_deleted',)


class FavouriteFeedAdmin(admin.ModelAdmin):
    list_display = ('user', 'added_on', 'is_deleted')
    search_fields = ('user',)
    list_filter = ('is_deleted',)


admin.site.register(models.Feed, FeedAdmin)
admin.site.register(models.LikedFeed, LikedFeedAdmin)
admin.site.register(models.FavouriteFeed, FavouriteFeedAdmin)
