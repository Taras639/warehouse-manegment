import unittest
from io import StringIO
from unittest.mock import patch
from tabulate import tabulate
from main import Product, FoodProduct, NonFoodProduct, Warehouse


class TestWarehouseManagementSystem(unittest.TestCase):

    def test_product_creation(self):
        # Test creating Product instance
        product = Product('SampleProduct', 10.0, 20, 'Producer')
        self.assertEqual(product.name, 'SampleProduct')
        self.assertEqual(product.cost, 10.0)
        self.assertEqual(product.quantity, 20)
        self.assertEqual(product.producer, 'Producer')

    def test_food_product_creation(self):
        # Test creating FoodProduct instance
        food_product = FoodProduct('FoodProduct', 5.0, 10, 'FoodProducer', 30)
        self.assertEqual(food_product.name, 'FoodProduct')
        self.assertEqual(food_product.cost, 5.0)
        self.assertEqual(food_product.quantity, 10)
        self.assertEqual(food_product.producer, 'FoodProducer')
        self.assertEqual(food_product.expiry_date, 30)

        # Test decrease_cost method
        food_product.expiry_date = 0.1  # Setting a low expiry date
        food_product.decrease_cost()
        self.assertEqual(food_product.cost, 4.5)  # Cost should be decreased by 10%

    def test_non_food_product_creation(self):
        # Test creating NonFoodProduct instance
        non_food_product = NonFoodProduct('NonFoodProduct', 15.0, 5, 'NonFoodProducer', 120, 'Purpose')
        self.assertEqual(non_food_product.name, 'NonFoodProduct')
        self.assertEqual(non_food_product.cost, 15.0)
        self.assertEqual(non_food_product.quantity, 5)
        self.assertEqual(non_food_product.producer, 'NonFoodProducer')
        self.assertEqual(non_food_product.dimensions, 120)
        self.assertEqual(non_food_product.purpose, 'Purpose')

        # Test decrease_cost method
        non_food_product.decrease_cost()
        self.assertEqual(non_food_product.cost, 16.5)  # Cost should be increased by 10%

    def test_warehouse_management(self):
        # Create a warehouse instance
        warehouse = Warehouse()

        # Test adding a FoodProduct
        food_product = FoodProduct('Apple', 2.0, 100, 'ProducerA', 10)
        warehouse.products.append(food_product)
        self.assertEqual(len(warehouse.products), 1)

        # Test adding a NonFoodProduct
        non_food_product = NonFoodProduct('Chair', 50.0, 10, 'ProducerB', 120, 'Furniture')
        warehouse.products.append(non_food_product)
        self.assertEqual(len(warehouse.products), 2)

        # Test showing product groups (mocking print)
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            warehouse.show_product_groups()
            output = mock_stdout.getvalue()
            # Checking if the output contains expected content
            self.assertIn("Apple", output)
            self.assertIn("Chair", output)

        # Other methods in warehouse can be tested in a similar manner


if __name__ == '__main__':
    unittest.main()
