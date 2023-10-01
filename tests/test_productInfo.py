import pytest 
from dotenv import load_dotenv

from src.modules.productInfo import getNegativeReviews, getPositiveReviews,getProductDetail,getProductDeals,getPros,getCons

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.simplefilter("error", DeprecationWarning)

class TestClass:
    

    # def test_getNegativeReviews(self):
    # 	productmodel = "GoPro Hero11"
    # 	negativereview = getNegativeReviews(productModel=productmodel)
    # 	print("negative review")
    # 	print(negativereview)
    # 	assert len(negativereview)>0
    # def test_getPositiveReviews(self):
    # 	productmodel = "GoPro Hero11"
    # 	positivereview = getPositiveReviews(productModel=productmodel)
    # 	print("positive review")
    # 	print(positivereview)
    # 	assert len(positivereview)>0
    def test_getPros(self):
        productmodel = "GoPro Hero11"
        pros_object = getPros(productModel=productmodel)
        print('pros')
        print(pros_object.pros)
        assert len(pros_object.pros)>=5 
        assert pros_object.name ==productmodel
    
    def test_getCons(self):
        productmodel = "GoPro Hero11"
        cons_object = getCons(productModel=productmodel)
        print('cons')
        print(cons_object.cons)
        assert len(cons_object.cons)>=5 
        assert cons_object.name ==productmodel
    
    def test_getProductDetail(self):
        productmodel = "GoPro Hero11"
        detail = getProductDetail(productModel=productmodel)
        print(detail.detail)
        assert len(detail.detail)>10
       

    
    
    