import streamlit as st
from src.modules.search import getProducts, ProductScope, ProductAttribute,getAttribute, getSerpProducts
from src.modules.productInfo import getPros, getCons, getProductDetail
from dotenv import load_dotenv
import pandas as pd
from dask.threaded import get

load_dotenv()

st.title("Recommer Linear Demo")

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
            print(product)
            # with columns[i%3]:
            
            st.title(product["title"])
            st.link_button(f"buy from {product['source']}",product["link"])
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    _df = pd.DataFrame([
                        {
                            "name":"title",
                            "value":product["title"]
                        },
                        {
                            "name":"price",
                            "value":product["price"]
                        },
                        {
                            "name":"source",
                            "value":product["source"]
                        },
                        {
                            "name":"rating",
                            "value":product["rating"]
                        },
                        {
                            "name":"store_rating",
                            "value":product["store_rating"]
                        },

                        ])
                   
                    
                    st.table(_df)
                    
                with col2:
                    st.image(product["thumbnail"])
                dsk = {'product_title': product["title"],
                    'pros': (getPros, 'product_title'),
                    'cons': (getCons, 'product_title'),
                    "details":(getProductDetail, 'product_title')}

                pros,cons,details = get(dsk, ["pros","cons","details"])
                st.write(details.detail)

                pros_col, cons_col = st.columns(2)
                with pros_col:
                    st.subheader("Pros")
                    if pros is None:
                        st.write("Not Avaliable")
                    else:
                        for pro in pros.pros:
                            st.markdown(f"- {pro}")
                with cons_col:
                    st.subheader("Cons")
                    if cons is None:
                        st.write("Not Avaliable")
                    else:
                        for con in cons.cons:
                            st.markdown(f"- {con}")
                    

                
                
            
            
        submit_select_product = st.form_submit_button(label="Submit")


