from django.contrib import admin
from .models import *
from django.forms import *
from django.utils.safestring import mark_safe

# Register your models here.


class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'photo', 'created_at', 'views', 'get_photo')
    list_display_links = ('id', 'user', 'content', 'photo', 'created_at', 'views')
    search_fields = ('user', 'content')
    # list_editable = ()
    list_filter = ('user', 'content', 'created_at')
    fields = ('user', 'content', 'photo', 'created_at', 'views', 'get_photo_big')
    readonly_fields = ('user', 'created_at', 'views', 'get_photo_big')
    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'

    def get_photo_big(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="350">')
        else:
            return '-'

    get_photo_big.short_description = 'Текущее изображение'


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'content', 'created_at')
    list_display_links = ('id', 'user', 'post', 'content', 'created_at')
    search_fields = ('user', 'post', 'content')
    # list_editable = ()
    list_filter = ('user', 'post', 'content')
    fields = ('user', 'post', 'content', 'created_at')
    readonly_fields = ('user', 'created_at')
    save_on_top = True


admin.site.register(Profile)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Follow)
admin.site.register(Comments, CommentsAdmin)
