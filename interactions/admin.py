from django.contrib import admin
from .models import Reaction, Comment


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'album', 'reaction_type', 'created_at')
    list_filter = ('reaction_type',)
    search_fields = ('user__username', 'album__title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'album', 'comment_text', 'parent_comment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'album__title', 'comment_text')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['delete_selected']
