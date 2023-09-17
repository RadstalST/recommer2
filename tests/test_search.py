
import pytest
from dotenv import load_dotenv

from  src.modules.search import getProducts, ProductScope, ProductAttribute,getAttribute, getSerpProducts
class TestClass:
    # for testing the function getProducts
    def TestClass(self):
        pass
    def test_getProducts(self):
        info = ProductScope(desire="I want to buy a car", tags=["fast", "hatchback"],description="for my family")
        products = getProducts(info,verbose=True)
        print(products)
        assert len(products.products) >= 5
    def test_getAttribute(self):
        cat = "keyboard"
        attributes = getAttribute(cat)
        print(attributes)

    def test_serpProducts(self):
        info = ProductScope(desire="I want to buy a car", tags=["fast", "hatchback"],description="for my family")
        products = getProducts(info,verbose=True)
        print(products)
        assert len(products.products) >= 5

        serp_results = getSerpProducts(products=products)
        print(serp_results)

        for res in serp_results:
            # assert if error
            if res.get("error"):
                assert False
  
        

    # def test_integration(self):
    #     desire = "I want to buy a car"
    #     attributes = getAttribute(desire)

    #     tags = attributes.list_attribute
    #     info = ProductScope(desire=desire, tags=tags, description="for my family")
    #     products = getProducts(info, verbose=True)
    #     print(products)

    #     serp_results = getSerpProducts(products=products, verbose=True)
    #     print(serp_results)


        
		

		


        
