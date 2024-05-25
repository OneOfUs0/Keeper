
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

def stop_onclick():
    # STOP          STOP         STOP

    print('STOP RUN')

    if st.session_state.status == 'working':
        st.session_state.status = 'resting'
        st.session_state.stoptime = datetime.datetime.now()
        print('Stopped timer')


    # calculate elapsed time

    # record the time elapsed on that project.

def start_onclick():
    # START         START         START

    print('START RUN')

    # START
    if st.session_state.status == 'resting':
        st.session_state.status = 'working'
        st.session_state.starttime = datetime.datetime.now()
        print('Started timer')


# ===============================  UI  ===========================================
# LAYOUT
st.title('Project Time Keeper')

st.divider()
cont_startstop = st.container()

cont_startstop.subheader(st.session_state.status)

if st.session_state.status == 'rest':
    notworking = True
    notresting = False

if st.session_state.status == 'work':
    notworking = False
    notresting = True


startwork = cont_startstop.button('Start',key='btn_start',on_click=start_onclick(),disabled=False)
stopwork = cont_startstop.button('Stop',key='btn_stop',on_click=stop_onclick(),disabled=False)


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
