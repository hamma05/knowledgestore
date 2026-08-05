from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html

from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_staff', 'is_active')
class BookAdmin(admin.ModelAdmin): 
    list_display = ('title', 'author', 'price', 'cover_preview')
    search_fields = ('title', 'author')
    list_filter = ('author',)

    def cover_preview(self, obj):
        image_src = None

        if obj.image:
            image_src = obj.image.url
        elif obj.urlimg:
            image_src = obj.urlimg if obj.urlimg.startswith('/') else static(obj.urlimg)

        if image_src:
            return format_html(
                '<img src="{}" alt="{}" style="width: 45px; height: 60px; object-fit: cover; border-radius: 4px;">',
                image_src,
                obj.title,
            )
        return 'No image'

    cover_preview.short_description = 'Cover'
class PanierAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'quantity')
    search_fields = ('user__username', 'book__title')
    list_filter = ('user', 'book')


class les_Commandes(admin.ModelAdmin):
    list_display= ('book','quantity')



admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Panier, PanierAdmin)
admin.site.register(CommandeBooks, les_Commandes)


