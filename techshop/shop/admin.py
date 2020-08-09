from django.contrib import admin
from . import models
# Register your models here.

def make_active(self, request, queryset):
    queryset.update(active=True)


make_active.short_description = "Mark selected items as active"


def make_inactive(self, request, queryset):
    queryset.update(active=False)


make_inactive.short_description = (
    "Mark selected items as inactive"
)
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "in_stock", "price", "old_price")
    list_filter = ("active", "in_stock", "date_updated")
    list_editable = ("in_stock",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("tags",)
    actions = [make_active, make_inactive]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return list(self.readonly_fields) + ["slug", "name"]

    def get_prepopulated_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.prepopulated_fields
        else:
            return {}

@admin.register(models.ProductReview)           
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'title', 'date', 'rating', 'is_approved')
    list_per_page = 20
    list_filter = ('product', 'user', 'is_approved')
    ordering = ['date']
    search_fields = ['user','content','title']
    
@admin.register(models.ProductCategory)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)
    
@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("thumbnail_tag", "product_name")
    readonly_fields = ("thumbnail",)
    search_fields = ("product__name",)

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="%s"/>' % obj.thumbnail.url
            )
        return "-"

    thumbnail_tag.short_description = "Thumbnail"

    def product_name(self, obj):
        return obj.product.name

@admin.register(models.ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(models.ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "timestamp",)
    list_filter = ("active",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return list(self.readonly_fields) + ["slug", "name"]

    def get_prepopulated_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.prepopulated_fields
        else:
            return {}