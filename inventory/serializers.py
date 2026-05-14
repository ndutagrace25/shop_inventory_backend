from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    profit_per_unit = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True
    )
    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "category_name",
            "name",
            "sku",
            "unit_cost",
            "selling_price",
            "quantity_on_hand",
            "reorder_level",
            "is_active",
            "profit_per_unit",
            "is_low_stock",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "category_name",
            "profit_per_unit",
            "is_low_stock",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        unit_cost = attrs.get("unit_cost", getattr(self.instance, "unit_cost", None))
        selling_price = attrs.get(
            "selling_price",
            getattr(self.instance, "selling_price", None)
        )

        if unit_cost is not None and selling_price is not None:
            if selling_price < unit_cost:
                raise serializers.ValidationError(
                    {
                        "selling_price": "Selling price cannot be lower than unit cost."
                    }
                )
        return attrs
