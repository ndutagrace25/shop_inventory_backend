from django.contrib import admin # type: ignore
from .models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "sku",
        "category",
        "unit_cost",
        "selling_price",
        "profit_per_unit",
        "quantity_on_hand",
        "reorder_level",
        "is_active",
        "created_at"
    )

    list_filter = ("category", "is_active")

    search_fields = ("name", "sku")
