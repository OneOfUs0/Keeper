
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


# ================================== CALLBACKS =========================================
def GenerateTimeReport():
    pass

# ===============================  UI  ===========================================

st.title('Report')

st.button('Generate Report',
          key='btn_report',
          on_click=GenerateTimeReport)