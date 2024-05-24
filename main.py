# This is a sample Python script.
import datetime
import streamlit as st
# import pandas as pd

# -------------------- development notes --------------------
#  To run this from Pycharm, do this:
#   1. open in PyCharm - (already here)
#  2.  go to the Terminal and type "streamlit run main.py"
#  To refresh the app, use F5.
#
#
# ---------------------------------------------------------

def start_onclick():
    print('starting timer')
    # record the start time.
    _starttime = datetime.datetime.now()

    now = datetime.datetime.now()


def stop_onclick():
    print('stopping timer')
    # calculate elapsed time

    # record the time elapsed on that project.


# LAYOUT
st.title('Project Time Keepers')
st.divider()
contain = st.container()
contain.button('inside')
contain.button('inside right', disabled=True)

btn_start = st.button('Start',on_click=start_onclick())
btn_stop = st.button('Stop',on_click=stop_onclick(),disabled=True)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    global _starttime



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
