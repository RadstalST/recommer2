import streamlit as st
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import json
from geopy.geocoders import Nominatim
import os
geolocator = Nominatim(user_agent=os.getenv("NOMATIM_USER_AGENT","some_user_agent@gmail.com")) # replace with your email

st.write(f"User agent is _{streamlit_js_eval(js_expressions='window.navigator.userAgent', want_output = True, key = 'UA')}_")

st.write(f"Screen width is _{streamlit_js_eval(js_expressions='screen.width', want_output = True, key = 'SCR')}_")

st.write(f"Browser language is _{streamlit_js_eval(js_expressions='window.navigator.language', want_output = True, key = 'LANG')}_")

st.write(f"Page location is _{ streamlit_js_eval(js_expressions='window.location.origin', want_output = True, key = 'LOC')}_")

# Copying to clipboard only works with a HTTP connection

copy_to_clipboard("Text to be copied!", "Copy something to clipboard (only on HTTPS)", "Successfully copied" , component_key = "CLPBRD")

# Share something using the sharing API
create_share_link(dict({'title': 'streamlit-js-eval', 'url': 'https://github.com/aghasemi/streamlit_js_eval', 'text': "A description"}), "Share a URL (only on mobile devices)", 'Successfully shared', component_key = 'shdemo')
                

if st.checkbox("Check my location"):
    loc = get_geolocation()
    st.write(f"Your coordinates are {loc}")

    location=geolocator.reverse((loc["coords"]["latitude"],loc["coords"]["longitude"]))
    st.write(f'Your city is {location}')
    address = location.raw['address']
    st.write(f'Your country is {address.get("country", "")}')
    st.write(f'Your state is {address.get("state", "")}')
    st.write(f'Your city is {address.get("city", "")}')
    st.write(f'Your postcode is {address.get("postcode", "")}')
    st.write(f'Your country code is {address.get("country_code", "")}')

    