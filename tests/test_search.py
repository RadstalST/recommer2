
import pytest
from dotenv import load_dotenv

from  src.modules.search import getProducts, ProductScope, productAttribute,getAttribute
class TestClass:
    # for testing the function getProducts
    def TestClass(self):
        pass
    def test_function(self):
        info = ProductScope(desire="I want to buy a car", tags=["fast", "hatchback"],description="for my family")
        products = getProducts(info,verbose=True)
        print(products)
        assert len(products.products) >= 5
	def test_attribute(self):
		cat = "keyboard"
		


        
