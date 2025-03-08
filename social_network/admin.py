from django.contrib import admin
from .models import Profile, Post, Category


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


