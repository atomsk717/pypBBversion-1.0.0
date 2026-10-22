from django.contrib import admin
from .models import Category, Forum, Topic, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_restricted', 'order')
    list_filter = ('category', 'is_restricted')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'forum', 'author', 'is_locked', 'created_at')
    list_filter = ('forum', 'is_locked')
    search_fields = ('title',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'author', 'created_at')
    list_filter = ('topic', 'author')