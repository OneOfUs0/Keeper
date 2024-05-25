
import datetime
import streamlit as st
import random
import pandas as pd
import string

# -------------------- development notes --------------------
#  To run this from Pycharm, do this:
#   1. open in PyCharm - (already here)
#  2.  go to the Terminal and cd to this folder.
#  3. type "streamlit run main.py"
#  4. on the app, set setting to "Run on Save"
#
# ---------------------------------------------------------

# ================================== INIT  =========================================

# initialize
if 'status' not in st.session_state:
    st.session_state.status = 'resting'
    print('----> init status')
if 'starttime' not in st.session_state:
    st.session_state.starttime = ''
if 'stoptime' not in st.session_state:
    st.session_state.stoptime = ''

if 'counter' not in st.session_state:
    st.session_state.counter = 0

if 'startstop_text' not in st.session_state:
    st.session_state.startstop_text = 'XXX'

# ================================== FUNCTIONS =========================================

@st.cache_data
def GetProjects():

    records = []
    for i in range(0,10):
        code = ''
        for cc in range(0,4):
            for c in range(0,3):
                code += str(random.randint(2,99))
            code += '.'

        name = ''
        for x in range(0,25):
            name += list(string.ascii_lowercase)[random.randint(0,23)]
        rec = {'code':code.strip('.'),'name':name}

        records.append(rec)

    df = pd.DataFrame(records)
    return df

# ================================== UI CALLBACKS =========================================

def startstop_onclick(status):

    if status == 'working':
        st.session_state.status = 'resting'
        st.session_state.stoptime = datetime.datetime.now()
        print('Stopped timer')
        st.session_state.counter += 1

        st.session_state.startstop_text = 'Start'

    if status == 'resting':
        st.session_state.status = 'working'
        st.session_state.starttime = datetime.datetime.now()
        print('Started timer')
        st.session_state.counter += 1

        st.session_state.startstop_text = 'Stop'


# ===============================  UI  ===========================================
# LAYOUT
st.title('Project Time Keeper')

st.divider()

st.subheader(st.session_state.status)

st.button(st.session_state.startstop_text,key='btn_startstop',on_click=startstop_onclick(st.session_state.status))


st.divider()

st.dataframe(GetProjects(),use_container_width=True)

cont_newProject = st.container()
cont_newProject.subheader("Add New Project Information")
cont_newProject.text_input('Billing Code',key='ti_newcode')
cont_newProject.text_input('Name (what you want to call it',key='ti_newname')

# ===============================  MAIN  ===========================================

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print('---- MAIN ----')
    print('status:' + st.session_state['status'])


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
