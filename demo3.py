import streamlit as st
from src.modules.search import getProducts, ProductScope, ProductAttribute,getAttribute, getSerpProducts
from src.modules.productInfo import getPros, getCons, getProductDetail
from dotenv import load_dotenv
import pandas as pd
from dask.threaded import get

def getlist(lists):
    liststr = ''
    for i in lists:
        liststr=liststr+'<li>'+i+'</li>'
    return liststr

        

def card(name,img,pros,cons,description,price,rating):
    prolist = getlist(pros)
    conlist = getlist(cons)
    return f"""
    <div class="card">
    <div class="card-body">
    <div class="row">
    <div class="col-sm">
        <h5 class="card-title">{name}</h5>
        <img src="{img}" class="img-thumbnail">
        <h6>rating: {rating}</h6>
    </div>
    <div class="col-sm-8">
    <h6>Description</h6>
        <p>{description}</p>
        <div class="card">
        <div class="card-body">
          <h5>Pros</h5>
          {prolist}
        </div>
        </div>
        <br>
        <div class="card">
        <div class="card-body">
          <h5>Cons</h5>
          {conlist}
        </div>
        </div>
        
    </div>
    <div class="col-sm">
        <h5>price: {price}</h5>
        <br>
        <button type="button" class="btn btn-dark">Sales Channel Detail</button>
    </div>
    </div>
    </div>
    </div>
"""

load_dotenv()
st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
""",unsafe_allow_html=True)
st.title("Recommer.Ai")

getAttribute = st.cache_data(getAttribute)
# getProducts = st.cache_data(getProducts)
if "desire" not in st.session_state:
    st.session_state.desire = None

if "attributes" not in st.session_state:
    st.session_state.attributes = None

with st.form(key="desireform"):
    desire = st.text_input(label="What do you want?")
    submitted_desire_form = st.form_submit_button(label="Submit")
    if submitted_desire_form:
        st.session_state.desire = desire

    if st.session_state.desire is not None:
        with st.status(f"AI: Loading related Product Attributes... : {desire}"):
            
            st.write("Loading the product attributes...")
            attributes = getAttribute(st.session_state.desire)
            
            st.session_state.attributes = attributes



if st.session_state.attributes is not None :

    with st.form(key="attribute_form"):
        description_field = st.text_input(label="more context")
        cols = st.columns(3)

        if "attribute_form_value" not in st.session_state:
            attribute_form_value = dict()
        else:
            attribute_form_value = st.session_state.attribute_form_value
        for i, variation in enumerate(attributes.list_variations):
            with cols[i%3]:
                attribute_form_value[variation] = st.checkbox(variation)


        submitted_attribute_form = st.form_submit_button(label="Submit")

    if "attribute_form_value" not in st.session_state:
        st.session_state.attribute_form_value = attribute_form_value

    if submitted_attribute_form:
        st.session_state.attribute_form_value = attribute_form_value
        productScope = ProductScope(
            desire=st.session_state.desire, 
            tags=[k for k,v in st.session_state.attribute_form_value.items() if v==True],
            description=description_field
            )
        with st.status("AI..."):
            st.json(productScope.dict())
            st.write("Searching for data...")
            st.session_state.products = getProducts(productScope)




    if "products" in st.session_state:
        with st.expander("debug"):
            st.markdown(st.session_state.products)
        with st.status("AI..."):
         st.write("Serping Data...")
         serpProducts = getSerpProducts(products=st.session_state.products)
        with st.form(key="select_product_form"):
            for i, product in enumerate(serpProducts):
                dsk = {'product_title': product["title"],
                     'pros': (getPros, 'product_title'),
                     'cons': (getCons, 'product_title'),
                     "details":(getProductDetail, 'product_title')}

                pros,cons,details = get(dsk, ["pros","cons","details"])
                pro_list = []
                con_list = []
                if pros is None:
                    pro_list.append("Pros Not available")
                else:
                    for p in pros.pros:
                        pro_list.append(p)
                
                if cons is None:
                    con_list.append("Cons not available")
                else:
                    for c in cons.cons:
                        con_list.append(c)



                st.markdown(card(product["title"],product["thumbnail"],pro_list,con_list,details.detail,product["price"],product["rating"]),unsafe_allow_html=True)
                st.markdown("***")
                

            print(product)
          
                
                
            
            
#         submit_select_product = st.form_submit_button(label="Submit")


