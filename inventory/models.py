from django.db import models # type: ignore
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity_on_hand = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    @property
    def profit_per_unit(self):
        return self.selling_price - self.unit_cost
    
    @property
    def is_low_stock(self):
        return self.quantity_on_hand <= self.reorder_level
    
    @property
    def stock_value(self):
        return self.quantity_on_hand * self.unit_cost
    
    def clean(self):
        if(self.unit_cost <0):
            raise ValidationError({"unit_cost": "Unit cost cannot be negative"})
        if(self.selling_price < 0):
            raise ValidationError({"selling_price": "Selling price cannot be negative"})
        if(self.selling_price < self.unit_cost):
            raise ValidationError({"selling_price": "Selling price cannot be lower than unit cost"})

