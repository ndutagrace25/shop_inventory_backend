from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Category, Product

class ProductModelTests(TestCase):
    def setUp(self):
        """
        Runs before every test.
        Used to create reusable test data
        """

        self.category = Category.objects.create(
            name="TEST CATEGORY",
            description="Testing category",
        )

    def test_profit_per_unit(self):
        """
        Product profit should equal:
        selling_price - unit_cost
        """

        product = Product.objects.create(
            category=self.category,
            name="TEST PRODUCT",
            sku="TEST001",
            unit_cost=Decimal("50.00"),
            selling_price=Decimal("80.00"),
            quantity_on_hand=10,
            reorder_level=5,
        )

        self.assertEqual(
            product.profit_per_unit,
            Decimal("30.00")
        )

    def test_low_stock_detection(self):

        """
        Product should be considered low stock 
        if quantity_on_hand <= reorder_level
        """

        product=Product.objects.create(
            category=self.category,
            name="LOW STOCK PRODUCT",
            sku="LOW001",
            unit_cost=Decimal("20.00"),
            selling_price=Decimal("40.00"),
            quantity_on_hand=3,
            reorder_level=5,
        )

        self.assertTrue(
            product.is_low_stock
        )

    def test_selling_price_cannot_be_lower_than_cost(self):

        """
        Validation should fail if
        selling price is lower than unit cost
        """

        product = Product.objects.create(
            category=self.category,
            name="INVALID PRODUCT",
            sku="BAD001",
            unit_cost=Decimal("40.00"),
            selling_price=Decimal("20.00"),
            quantity_on_hand=30,
            reorder_level=5,
        )

        with self.assertRaises(ValidationError) as context:
            product.full_clean()


        self.assertEqual(
            context.exception.message_dict["selling_price"][0],
            "Selling price cannot be lower than unit cost"
        )