from django.tests import TestCase
#from .restaurant import models
class MenuItemTest(TestCase):
    def test_get_item(self):
        item = MenuItem.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(item, "IceCream : 80")


class MenuViewTest(TestCase):
    def setup(self):
        menuItem=MenuItem.objects.create{
            "title": "Beef Bolognese",
            "price": 45.00,
            "featured": false,
            "category": 1, }
        item=menuItem.objects.all()
    self.assertEqual(item, "Beef Bolognese : 45.00")
    
