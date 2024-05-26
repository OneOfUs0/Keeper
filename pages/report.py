
import streamlit as st
# import random
# import pandas as pd
# import string
# import datetime

st.set_page_config(page_title='Report Times',
                   page_icon=':stopwatch:',
                   menu_items={
                       'Report a Bug':'https://www.google.com/appserve/security-bugs/m2/new',
                       'Get Help':'https://somafm.com/dronezone',
                       'About':'Created by Greg Nichols'
                   })

# ================================== INIT  =========================================



# ================================== FUNCTIONS =========================================
def GenerateTimeReport():
    pass

# ================================== CALLBACKS =========================================


# ===============================  UI  ===========================================

st.title('Report')

st.button('Generate Report',on_click=GenerateTimeReport())