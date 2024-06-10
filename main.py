import  traceback, sys, os
import random
import pandas as pd
import string
import datetime
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

#from google_cloud_firestore.base_query import FieldFilter
#from google_cloud_firestore import FieldFilter

import streamlit as st
# from streamlit import st.experimental_dialog

# THIS IS TO ALLOW ONLY ME TO ACCESS SINCE I HAVE THE CREDENTIALS CERTIFICATE.
# r'C:\Users\36352\PycharmProjects\Keeper\tkeeper-c0270-firebase-adminsdk-ou3gc-03d4e1ddde.json'

#CertFolder = r'C:\Users\36352\PycharmProjects\Keeper'
#FIREBASE_CERTIFICATE_FILE = os.path.join(CertFolder,'tkeeper-c0270-firebase-adminsdk-ou3gc-03d4e1ddde.json')

CertFolder = r'C:\firebase'
FIREBASE_CERTIFICATE_FILE = os.path.join(CertFolder,'tkeeper_firebase_cert.json')


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
                   layout="wide",
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
if 'df_projects' not in st.session_state:
    df = pd.DataFrame()
    st.session_state.df_projects = df

if 'starttime' not in st.session_state:
    st.session_state.starttime = ''
if 'stoptime' not in st.session_state:
    st.session_state.stoptime = ''

if 'comment' not in st.session_state:
    st.session_state.comment = ''
if 'txt_comment' not in st.session_state:
    st.session_state.txt_comment = ''

if 'status' not in st.session_state:
    st.session_state.status = 'rest'

if 'active_project_code' not in st.session_state:
    st.session_state.active_project_code = '0'

if 'active_project_name' not in st.session_state:
    st.session_state.active_project_name = ''

if 'collection_present' not in st.session_state:
    st.session_state.collection_present = False

# DATABASE  -------------
if 'app_initialized' not in st.session_state:
    st.session_state.app_initialized = False


if not os.path.exists(FIREBASE_CERTIFICATE_FILE):
    print('Firebase Certificate file not found.  You must first get access to Firebase.')
    st.session_state.app_initialized = False
    # force the setup page to open and disable sidebar navigation.
    st.switch_page('pages/setup.py')
else:
    cred = credentials.Certificate(FIREBASE_CERTIFICATE_FILE)
    if not st.session_state.app_initialized:
        app = firebase_admin.initialize_app(cred)
        st.session_state.app_initialized = True
    db = firestore.client()

# check for database collections and documents.
# Create if missing.
if st.session_state.app_initialized and not st.session_state.collection_present:

    # test if "projects" collection.
    colref = db.collection('projects')
    if colref is not None:
        st.session_state.collection_present = True
    else:

        # PROJECTS
        doc_ref = db.collection('projects').document()
        doc_ref.set({'billcode': 0, 'projectname': '0'})

        # WORKLOG
        doc_ref = db.collection('worklog').document()
        now = datetime.datetime.now()
        date_ord = now.toordinal()
        adate = now.strftime('%m/%d/%Y')
        theday = now.strftime('%A')

        log_record = {'date_ord': date_ord, 'adate': adate, '': theday, 'projectname': '',
                      'billcode': '0', 'comment': '',
                      'elapsedtime': 0, 'userid': 0}
        doc_ref.set(log_record)

        st.session_state.collection_present = True


# NOTE: this is CACHED
@st.cache_data
def GetProjects_cloud():
    try:
        records = []

        docs = db.collection('projects').get()
        for doc in docs:
            record = doc.to_dict()
            records.append(record)

        df = pd.DataFrame(records)

        st.session_state.df_projects = df

        return df
    except:
        ExceptHandler()


def Database_Project_Add(billcode, projectname):
    try:
        # add to the database
        doc_ref = db.collection('projects').document()
        doc_ref.set({'billcode': billcode, 'projectname': projectname})

        #Trigger a refresh of the data editor widget.
        GetProjects_cloud()
        st.rerun()


    except:
        ExceptHandler()


@st.cache_data
def GetProjectsRandom():
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

        #date_ymd = st.session_state.stopdate.year + '-' + st.session_state.stopdate.month + '-' + st.session_state.stopdate.day
        date_ord = st.session_state.stopdate.toordinal()

        userid = '36353'

        # print('Worked for ' + str(int(elap_minutes)) + ' minutes on ' + st.session_state.comment)

        log_record = {'date_ord':date_ord, 'adate': thedate, 'aday': theday, 'projectname':projectname,
                      'billcode': billcode, 'comment': comment,
                      'elapsedtime': elapsedtime, 'userid': userid}

        #print(str(log_record))

        if st.session_state.btn_stop_clicked == True:
            Database_Log_Add(log_record)


    except:
        ExceptHandler()
def startworking():
    try:
        ### User has started working.   Record the start time. ###
        print('START WORKING!')

        # start time
        st.session_state.starttime = datetime.datetime.now()

        st.session_state.startdate = datetime.date.today()  #datetime.date

    except:
        ExceptHandler()
def stopworking():
    try:
        ### User has stopped working.  Add an entry to the worklog ###
        print('STOPPED WORKING')

        # stop time and date
        st.session_state.stoptime = datetime.datetime.now()
        st.session_state.stopdate = datetime.date.today()  # datetime.date

        # LOG billcode, time, and comments.
        st.session_state.btn_stop_clicked = True
        AddEntry()
        st.session_state.btn_stop_clicked = False

    except:
        ExceptHandler()
# ================================== CALLBACKS =========================================

def btn_click_ClearWork():
    try:
        ''' Clear ALL work history entries in the database.'''
        docs = db.collection('worklog').get()
        for doc in docs:
            key = doc.id
            db.collection('worklog').document(key).delete()
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
        print('NEW PROJECT SELECTION')

    except:
        ExceptHandler()
def DeleteSelectedProject():
    try:
        billcode = st.session_state.active_project_code

        # query the collection to get document(s)
        doc_refs = db.collection('projects').where(field_path='billcode',op_string='==',value=billcode).get()

        if len(doc_refs) == 0:
            print('None returned')
        else:
            for doc in doc_refs:
                docid = doc.id
                #print('Going to delete: ' + docid + ' ' + str(doc.to_dict()))

                db.collection('projects').document(docid).delete()
                print('Deleted document id' + docid)

        # trigger a refresh of the projects data editor
        st.rerun()
        #GetProjects_cloud()

    except:
        ExceptHandler()
def btnAddProject_click():
    try:
        NewProject_modal()
        # open the modal dialog to add the project
    except:
        ExceptHandler()

@st.experimental_dialog('Enter New Project Information',width='large')
def NewProject_modal():
    try:

        # FORM
        #with st.form('New Project Information', clear_on_submit=True):
        with st.container():
            # st.subheader("Add a New Project")
            newcode = st.text_input('Billing Code', key='ti_newcode')
            newname = st.text_input('Name (what you want to call it)', key='ti_newname')

            #submitted = st.form_submit_button('Submit',
              #                                disabled=bool(st.session_state.status == 'work'))

            submitted = st.button('Submit')
            if submitted:
                Database_Project_Add(newcode, newname)
                st.rerun()


    except:
        ExceptHandler()
def btnstartstop_click():
    try:
        if st.session_state.btnstop:
            # stop working.
            stopworking()
            st.session_state.status = 'rest'

        if st.session_state.btnstart:
            # start working
            startworking()
            st.session_state.status = 'work'


    except:
        ExceptHandler()

# ===============================  UI  ===========================================
try:

    tittlecol1, tittlecol2 = st.columns([5, 1])

    with tittlecol1:
        # TITLE
        st.subheader('Project Time Keeper')


    with tittlecol2:
        # BUTTON
        st.button('New Week (clear history)',
                  key='clearall',
                  on_click=btn_click_ClearWork,
                  help='Use with caution.  This will erase all your previous work history.')

    #st.divider()

    # ------- PROJECTS -----

    # SUBHEADER
    #st.subheader('Choose the Project:',
     #            help='Choose the project you will be working on.')


    # get pandas dataframe
    #df = GetProjectsRandom()
    df = GetProjects_cloud()
    df = st.session_state.df_projects

    # Add a true/false field to the first column.
    df_selections = df.copy()
    df_selections.insert(0, "Select", False)
    # configure the "Apply to this" column to have checkboxes
    column_config = {'Apply to this':st.column_config.CheckboxColumn(required=True)}

    column1, column2 = st.columns([10, 1])

    with column1:

        #DATA EDITOR     ['billcode','projectname'],
        edited_df = st.data_editor(df_selections,
                                   hide_index=True,
                                   column_config=column_config,
                                   use_container_width=True,
                                   on_change=data_editor_changed,
                                   disabled=bool(st.session_state.status == 'work')
                                   )

    # check for mulitple selections.
    sel_codes = edited_df.loc[edited_df['Select']]["billcode"]
    sel_names = edited_df.loc[edited_df['Select']]["projectname"]
    if len(sel_codes) == 0:
        st.session_state.active_project_code = '0'
        st.session_state.active_project_name = 'none'
    elif len(sel_codes) > 1:
        st.warning('Select only one Project.')
        st.session_state.active_project_code = '0'
        st.session_state.active_project_name = 'none'
    else:
        # save to session state
        st.session_state.active_project_code = sel_codes.iloc[0]
        st.session_state.active_project_name = sel_names.iloc[0]

    with column2:

        subcont = st.container()

        with subcont:
            # BUTTON
            btndisabled = (st.session_state.status == 'work') or (st.session_state.active_project_code == '0')
            st.button('Delete Selected Project',
                      key='btnClearSelected',
                      help='Delete the project you selected.',
                      on_click=DeleteSelectedProject,
                      disabled=btndisabled)


            st.button(':red-background[Add Another Project - Experimental WIP]',
                      key='btnAddProject',
                      help='Add a new project and billcode.',
                      disabled=bool(st.session_state.status == 'work'),
                      on_click=btnAddProject_click)

            # if st.session_state.btnAddProject:
            #     NewProject_modal()
            #     # open the modal dialog to add the project



    # ------------------------ add a new proejct ------------------------------------------------------
    with st.expander('Add a New Billing Code and Project',expanded=False):

        # FORM
        with st.form('New Project Information',clear_on_submit=True):
            st.subheader("Add a New Project")
            newcode = st.text_input('Billing Code',key='ti_newcode')
            newname = st.text_input('Name (what you want to call it)',key='ti_newname')

            submitted = st.form_submit_button('Submit',
                                              disabled=bool(st.session_state.status == 'work'))

            if submitted:
                if newcode == '' or newname == '':
                    st.warning('Billing Code and Name are required.')
                else:
                    Database_Project_Add(newcode, newname)
                    # Trigger an update of the data editor.


    # TEXTAREA
    st.text_area('Comments about tasks:',
                 key='txt_comment',
                 on_change=comment_changed,
                 max_chars=200,
                 help='Type comments for this work.')

    # ---------------------- start stop working --------------------------------------------------------------

    col1, col2 = st.columns([4, 1])

    st.session_state.active_project_name = 'This and That'

    with col1:
        # HEADER
        st.subheader(st.session_state.active_project_code,
                     help='The chosen project.')
        # st.subheader('Controls')  # st.session_state.status)

    #type(st.session_state['active_project_code'])

    with col2:
        # TOGGLE
        with st.container():

            # decide which buttons are enabled.

            if bool(st.session_state.active_project_code == '0'):
                disablestart = True
                disablestop = True
            else:
                if st.session_state.status == 'work':
                    disablestart = True
                    disablestop = False
                else:
                    disablestart = False
                    disablestop = True



            st.button('START',
                      type='primary',
                                key='btnstart',
                                  disabled=disablestart,
                                  help='Click to start working.',
                                  use_container_width=True,
                                  on_click=btnstartstop_click)

            st.button('STOP',
                      type='primary',
                      key='btnstop',
                                  disabled=disablestop,
                                  help='Click to stop working.',
                                  use_container_width=True,
                                  on_click=btnstartstop_click)



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
