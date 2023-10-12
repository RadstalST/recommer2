import streamlit as st
from src.modules.search import getProducts, ProductScope, ProductAttribute,getAttribute, getSerpProduct,ProductsLists
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
from src.modules import utils
import json
#init cache decorator
getAttribute = st.cache_data(getAttribute)
getProducts = st.cache_data(getProducts)

#init containers    
headerContainer = st.container()
st.divider()
desireContainer = st.container()
st.divider()
productOptionsContainer = st.container()
st.divider()
productListContainer = st.container()

#init user info

loc = get_geolocation()
if loc:
    latlong = (loc["coords"]["latitude"],loc["coords"]["longitude"])

else:
    latlong = (0,0) # default location

with st.sidebar:
    st.header("User Info")
    st.markdown(f"`{latlong}`")

    

with headerContainer:
    st.header("RecommerAI")
    st.markdown("This is a demo of RecommerAI")

with desireContainer:
    desire = st.text_input("I want ... *",value="Mechanical Keyboard")
    desire_to = st.text_input("I want to ... *",value="play games")
    desire_with = st.text_input("I want with ...",value="RGB")
    desire_for = st.text_input("I want for ...",value="my son")



    with st.form(key="desire_form"):
        submitted = False
        with st.chat_message("assistant"):
            message = ""
            if utils.isValidString(desire):
                message += f" `{desire}`"
            if utils.isValidString(desire_to):
                message += f" to `{desire_to}`"
            if utils.isValidString(desire_with):
                message += f" with `{desire_with}`"
            if utils.isValidString(desire_for):
                message += f" for `{desire_for}`"
            st.markdown(f"You want: {message}")
            

            if utils.isValidString(desire) and utils.isValidString(desire_to):
                st.write("is that correct?")
        if utils.isValidString(desire) and utils.isValidString(desire_to):
            with st.chat_message("user"):
                submitted = st.form_submit_button(label="Yes")
        else:
            submitted = st.form_submit_button(label="Please fill in the required fields", disabled=True)
        if submitted:
            with st.chat_message("assistant"):
                with st.status("AI: Loading related Product Attributes..."):
                    st.write("Loading the product attributes...")
                    attributes = getAttribute(desire)
                    st.session_state.attributes = attributes
                    st.write(attributes)


productContainers = dict()
if "attributes" in st.session_state:
    with productOptionsContainer:
        cols = st.columns(3)
        attributes_options = dict()

        if 'attributes_options' in st.session_state:
            attributes_options = st.session_state.attributes_options
        else:
            # attributes_options = dict with variation as key and value as boolean(false)    
            attributes = st.session_state.get("attributes")
            for i, variation in enumerate(attributes.list_variations):
                attributes_options[variation] = False
        for i, variation in enumerate(attributes_options.keys()):
            with cols[i%3]:
                attributes_options[variation] = st.checkbox(variation)

        st.session_state.attributes_options = attributes_options

        with st.form(key="attribute_form"):

            with st.chat_message("assistant"):
                selected_attributes = [k for k,v in attributes_options.items() if v==True]
                st.write(f"You want: \n\n{message or 'nothing'} \n\nwith the following attributes:")
                if len(selected_attributes) == 0:
                    st.markdown("`None`")
                else:
                    st.markdown("`"+"`, `".join(selected_attributes)+"`")
                        
            with st.chat_message("user"):
                st.write("I want products with those attributes")
                submitted_attrubute = st.form_submit_button(label="Submit")
            
            if submitted_attrubute:
                productScope = ProductScope(
                    desire=message, 
                    tags=selected_attributes,
                    description=""
                )
                with st.chat_message("assistant"):
                    with st.status("AI: Loading related Products..."):
                        st.write("Searching for data...")
                        st.session_state.products = getProducts(productScope,hash=productScope.model_dump_json())   
                        st.write(st.session_state.products)
                        st.write("Done")
                with st.chat_message("assistant"):
                    st.write("Here are the top products that matches description")
                    # st.write(st.session_state.products)
                    for product in ProductsLists(**json.loads(st.session_state.products)).products:
                        _key = "product_"+product.name
                        
                        with productListContainer:
                            productContainers[_key] = st.container()
                            with productContainers[_key]:
                                st.header(product.name)
                                st.caption(product.description)
                                st.subheader("Related Products")
                                with st.status("AI: Loading related Products..."):
                                    st.write("Searching for data...")
                                    related_products = getSerpProduct(product,hash=product.name,latlong=latlong)
                                    st.write(related_products)
                                    st.write("Done")
                        
                    st.write("Done")

