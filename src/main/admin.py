from django.contrib import admin
from .models import Stories, StoryVideos


class StoryVideosInline(admin.StackedInline):
    model = StoryVideos
    extra = 0


@admin.register(Stories)
class StoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    list_display_links = list_display
    inlines = (StoryVideosInline,)
