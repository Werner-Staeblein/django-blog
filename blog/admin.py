from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin

# This is the summernote Admin "model"
# This summernote Admin "model" is NOT (!) included in the models.py
# Because the Post Model is now included in the Admin model
# as an argument, the Post model does not have to be registered
# separately any longer and the former entry of 
# admin.site.register(Post) was deleted

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

# Register your models here.
admin.site.register(Comment)
