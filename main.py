import  traceback, sys
import streamlit as st
import random
import pandas as pd
import string
import datetime

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials


def ExceptHandler():
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    print(pymsg)


# -------------------- development notes --------------------
#  To run this from Pycharm, do this:
#   1. open in PyCharm - (already here)
#  2.  go to the Terminal and cd to this folder.
#  3. type "streamlit run main.py"
#  4. on the app, set setting to "Run on Save"
#
# ---------------------------------------------------------

#  THIS METHOD ALLOWS ANYONE WHO IS USING THE TKEEPER APPLICATION TO ACCESS.
# Configuration key
# firebaseConfig = {
#     'apiKey'': "AIzaSyDMiFm1gWW2_XA6Ax9aFOmv_kfB1lDn3Y8",
#     'authDomain': "tkeeper-c0270.firebaseapp.com",
#     'projectId': "tkeeper-c0270",
#     'databaseURL':'firebase-adminsdk-ou3gc@tkeeper-c0270.iam.gserviceaccount.com',
#     'storageBucket'': "tkeeper-c0270.appspot.com",
#     'messagingSenderId': "744297028887",
#     'appId': "1:744297028887:web:84633b8788aad111402b52",
#     'measurementId': "G-3RCJB966V0"
# }
#
# # initialize the connection to the firestore database.
# app = firebase_admin.initialize_app(firebaseConfig)

# ================================== INIT  =========================================

# Page
st.set_page_config(page_title='Time Keeper Controls',
                   page_icon=':stopwatch:',
                   menu_items={'About':'Created by Greg Nichols',
                               'Get Help':'https://somafm.com/dronezone/'})

# initialize

# FLOW CONTROL  -----------
if 'status' not in st.session_state:
    st.session_state.status = 'You are not working'
    print('----> init status')

if 'btn_stop_clicked' not in st.session_state:
    st.session_state.btn_stop_clicked = False

# VALUES   -----------

if 'starttime' not in st.session_state:
    st.session_state.starttime = ''
if 'stoptime' not in st.session_state:
    st.session_state.stoptime = ''

if 'comment' not in st.session_state:
    st.session_state.comment = ''
if 'txt_comment' not in st.session_state:
    st.session_state.txt_comment = ''

if 'startstop_text' not in st.session_state:
    st.session_state.startstop_text = 'Toggle to Start working'

if 'active_project_code' not in st.session_state:
    st.session_state.active_project_code = '0'
if 'active_project_name' not in st.session_state:
    st.session_state.active_project_name = ''

# DATABASE

if 'app_initialized' not in st.session_state:
    st.session_state.app_initialized = False

# THIS IS TO ALLOW ONLY ME TO ACCESS SINCE I HAVE THE CREDENTIALS CERTIFICATE.
cred = credentials.Certificate(r'C:\Users\36352\PycharmProjects\Keeper\tkeeper-c0270-firebase-adminsdk-ou3gc-03d4e1ddde.json')

if not st.session_state.app_initialized:
    app = firebase_admin.initialize_app(cred)
    st.session_state.app_initialized = True

db = firestore.client()

# ================================== FUNCTIONS =========================================
@st.cache_data
def GetProjects_cloud():
    try:
        records = []

        docs = db.collection('projects').get()
        for doc in docs:
            record = doc.to_dict()
            records.append(record)

        df = pd.DataFrame(records)

        return df
    except:
        ExceptHandler()


def Database_Project_Add(billcode, projectname):

    try:
        # add to the database
        doc_ref = db.collection('projects').document()
        doc_ref.set({'billcode': billcode, 'projectname': projectname})

    except:
        ExceptHandler()


@st.cache_data
def GetProjects():
    try:
        # Projects_dict = GetProjects_cloud()

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
            rec = {'billcode':code.strip('.'),'projectname':name}

            records.append(rec)

        df = pd.DataFrame(records)

        return df
    except:
        ExceptHandler()

def Database_Log_Add(log_record):
    try:
        # add

        doc_ref = db.collection('worklog').document()
        doc_ref.set(log_record)
    except:
        ExceptHandler()
def AddEntry():
    try:
        # LOG billcode, time, and comments.

        userid = ''

        billcode = st.session_state.active_project_code
        projectname = ''
        comment = st.session_state.comment

        start = st.session_state.starttime
        stop = st.session_state.stoptime

        thedate = stop.strftime('%m/%d/%Y')
        theday = stop.strftime('%A')
        td = stop - start
        elap_minutes = td.seconds / 60
        elapsedtime_hrs = elap_minutes / 60
        elapsedtime = '{:.4f}'.format(elapsedtime_hrs)

        userid = '36353'

        # print('Worked for ' + str(int(elap_minutes)) + ' minutes on ' + st.session_state.comment)

        log_record = {"adate": thedate, "aday": theday, 'projectname':projectname, 'billcode': billcode, 'comment': comment,
                      'elapsedtime': elapsedtime, 'userid': userid}

        print(str(log_record))

        # COMMENT OUT FOR TESTING
        if st.session_state.btn_stop_clicked == True:
            Database_Log_Add(log_record)


    except:
        ExceptHandler()
def startworking():
    try:
        print('START WORKING!')

        # start time
        st.session_state.starttime = datetime.datetime.now()

    except:
        ExceptHandler()
def stopworking():
    try:
        print('STOPPED WORKING')

        # stop time
        st.session_state.stoptime = datetime.datetime.now()

        # LOG billcode, time, and comments.
        st.session_state.btn_stop_clicked = True
        AddEntry()
        st.session_state.btn_stop_clicked = False

    except:
        ExceptHandler()
# ================================== CALLBACKS =========================================

def btn_click_ClearWork():
    try:
        docs = db.collection('worklog').get()

        for doc in docs:
            key = doc.id
            print(key)
            db.collection('worklog').document(key).delete()

    except:
        ExceptHandler()

def toggle_changed():
    try:

        if st.session_state.toggle_work == False:
            print('Toggle turned off')
            stopworking()
        else:
            print('Toggle turned on')
            startworking()

    except:
        ExceptHandler()

def comment_changed():
    try:

        thecomment = st.session_state.txt_comment
        st.session_state.comment = thecomment
        print('updated to ' + thecomment)

    except:
        ExceptHandler()
def data_editor_changed():
    try:
        print('NEW SELECTION')

    except:
        ExceptHandler()
# ===============================  UI  ===========================================
try:
    st.title('Project Time Keeper')

    st.button('Dev - clear work history',
              key='clearall',
              on_click=btn_click_ClearWork)

    #st.divider()

    # ------- COTROLS - StartStop, Comments -----
    st.subheader('Control work here.') #st.session_state.status)

    type(st.session_state['active_project_code'])

    onoff = st.toggle('Working',
                      key='toggle_work',
                      disabled=False,
                      help='Turn on when you start working.  Turn off when you stop working.',
                      on_change=toggle_changed
                      )


    st.text_area('Comments',key='txt_comment', on_change=comment_changed, max_chars=200,help='Type comments for this work.')


    # ------- PROJECTS -----
    st.subheader('Projects',
                 help='Choose the project you will be working on.')


    # get pandas dataframe
    #df = GetProjects()
    df = GetProjects_cloud()

    # Add a true/false field to the first column.
    df_selections = df.copy()
    df_selections.insert(0, "Apply to this", False)

    # configure the "Apply to this" column to have checkboxes
    column_config = {'Apply to this':st.column_config.CheckboxColumn(required=True)}

    # create the Data Editor
    edited_df = st.data_editor(df_selections,
                               hide_index=True,
                               column_config=column_config,
                               disabled=['billcode','projectname'],
                               use_container_width=True,
                               on_change=data_editor_changed
                               )

    # check for mulitple selections.
    sel_codes = edited_df.loc[edited_df['Apply to this']]["billcode"]
    sel_names = edited_df.loc[edited_df['Apply to this']]["projectname"]
    if len(sel_codes) == 0:
        st.session_state.active_project_code = '0'
        st.session_state.active_project_name = ''
    elif len(sel_codes) > 1:
        st.warning('Select only one Project.')
        st.session_state.active_project_code = '0'
        st.session_state.active_project_name = ''
    else:
        # save to session
        st.session_state.active_project_code=sel_codes.iloc[0]
        st.session_state.active_project_name = sel_names.iloc[0]

    # ------- NEW PROJECT -----
    with st.form('New Project Information',clear_on_submit=True):
        st.subheader("Add a New Project")
        newcode = st.text_input('Billing Code',key='ti_newcode')
        newname = st.text_input('Name (what you want to call it)',key='ti_newname')
        submitted = st.form_submit_button('Submit')
        if submitted:
            if newcode == '' or newname == '':
                st.warning('Billing Code and Name are required.')
            else:
                Database_Project_Add(newcode, newname)

except:
    ExceptHandler()

# ===============================  MAIN  ===========================================
try:
    # Press the green button in the gutter to run the script.
    if __name__ == '__main__':
        pass
        #print('---- MAIN ----')
except:
    ExceptHandler()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
