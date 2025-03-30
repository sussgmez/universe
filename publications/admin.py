from django.contrib import admin
from .models import Publication, Category


@admin.register(Publication)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
