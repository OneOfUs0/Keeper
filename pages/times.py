import  traceback, sys, os
import random
import pandas as pd
import string
import datetime
#from goodle_cloud_firestore import firestore
#from goodle_cloud_firestore import credentials
# import firebase_admin
# from firebase_admin import firestore
# from firebase_admin import credentials
import streamlit as st

#CertFolder = r'C:\firebase'
#FIREBASE_CERTIFICATE_FILE = os.path.join(CertFolder,'foo') #'tkeeper_firebase_cert.json')

def Refresh():
    GetProjects_cloud.clear()
    st.rerun()

def ExceptHandler():
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    print(pymsg)

# ------------------------------- INIT ---------------------------------

# Page
st.set_page_config(page_title='Time Keeper Controls',
                   layout="wide",
                   page_icon=':stopwatch:',
                   menu_items={'About':'Created by OneOfUs0, June 2024',
                               'Get Help':'https://somafm.com/dronezone/'})

try:
    # FLOW CONTROL
    if 'status' not in st.session_state:
        st.session_state.status = 'You are not working'

    if 'btn_stop_clicked' not in st.session_state:
        st.session_state.btn_stop_clicked = False

    # VALUES
    if 'df_projects' not in st.session_state:
        df = pd.DataFrame()
        st.session_state.df_projects = df

    if 'starttime' not in st.session_state:
        st.session_state.starttime = None #datetime.date
    if 'stoptime' not in st.session_state:
        st.session_state.stoptime = None  #datetime.date

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

    # if 'certfile' not in st.session_state:
    #     st.session_state.certfile = ''

    if 'collection_present' not in st.session_state:
        st.session_state.collection_present = False

    # DATABASE
    if not st.session_state.app_initialized:
        raise SystemExit(0)  # QUIT EXECUTION
    else:
        db = st.session_state.db

    #     cred = credentials.Certificate(st.session_state.certfile)
    #     if not st.session_state.app_initialized:
    #         app = firebase_admin.initialize_app(cred)
    #         st.session_state.app_initialized = True
    #     db = firestore.client()

    # Check for the existence of the database collection and documents.
    # If they are missing, create them.
    if st.session_state.app_initialized and not st.session_state.collection_present:

        print('CHECKING FOR EXISTING COLLECTIONS AND DOCUMENTS')

        # test if "projects" collection.
        cols = db.collections()

        found = False
        for col in cols:
            if col.id == 'projects':
                found = True
        if found:
            st.session_state.collection_present = True
        else:

            # PROJECTS
            print('Creating the projects collection.')
            doc_ref = db.collection('projects').document()
            doc_ref.set({'billcode': 0, 'projectname': '0'})

            # WORKLOG
            print('Creating the worklog collection.')
            doc_ref = db.collection('worklog').document()
            now = datetime.datetime.now()
            date_ord = now.toordinal()
            adate = now.strftime('%m/%d/%Y')
            theday = now.strftime('%A')

            log_record = {'date_ord': date_ord, 'adate': adate, 'none': theday, 'projectname': 'none',
                          'billcode': '0', 'comment': 'none',
                          'elapsedtime': 0, 'userid': 0}
            doc_ref.set(log_record)

            # # delete the bogus project and work document.
            # docs = db.collection('projects').get()
            # docid = '0'
            # for doc in docs:
            #     docid = doc.id
            # db.collection('projects').document(docid).delete()
            #
            # docs = db.collection('worklog').get()
            # docid = '0'
            # for doc in docs:
            #     docid = doc.id
            # db.collection('worklog').document(docid).delete()

            st.session_state.collection_present = True

except:
    ExceptHandler()

# ------------------------------- FUCNTIONS ---------------------------------
# NOTE: CACHED
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

        Refresh()

        # clear the cache for this function
        #GetProjects_cloud.clear()
        #st.rerun()
    except:
        ExceptHandler()

@st.cache_data
def GetProjectsRandom():
    try:
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

        date_ord = st.session_state.stopdate.toordinal()

        userid = '36353'

        # print('Worked for ' + str(int(elap_minutes)) + ' minutes on ' + st.session_state.comment)

        log_record = {'date_ord':date_ord, 'adate': thedate, 'aday': theday, 'projectname':projectname,
                      'billcode': billcode, 'comment': comment,
                      'elapsedtime': elapsedtime, 'userid': userid}

        #print(str(log_record))

        if st.session_state.btn_stop_clicked:
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
        #print('updated to ' + thecomment)

    except:
        ExceptHandler()

def dataframe_projects_select():
    try:
        sel_event = st.session_state.dataframe_projects
        selected = sel_event.selection

        df = st.session_state.df_projects
        D = df.to_dict(orient='records')  # <--- a list of dicts.

        if len(selected['rows']) == 1:
            idx = selected['rows'][0]
            st.session_state.active_project_name = D[idx]['projectname']
            st.session_state.active_project_code = D[idx]['billcode']

        if len(selected['rows']) == 0:
            st.session_state.active_project_name = ''
            st.session_state.active_project_code = '0'

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
        GetProjects_cloud.clear()
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
def btnBulkUpload_Click():
    try:
        thefile = st.session_state.btnBulkUpload
        if thefile is not None:

            # just go straight to a pandas dataframe.
            dfx = pd.read_csv(thefile)
            # and back out to a dictionary.
            D = dfx.to_dict(orient='records')

            for rec in D:
                newcode = rec['billcode']
                newname = rec['projectname']
                print('Adding code: ' + newcode + ' for project: ' + newname)

                # Add to the database.
                Database_Project_Add(newcode, newname)
    except:
        ExceptHandler()
def btnNavReport_Click():
    try:
        st.switch_page("pages/report.py")

    except:
        ExceptHandler()

# ===============================  UI  ===========================================
try:
    tittlecol1, tittlecol2 = st.columns([5, 1])

    with tittlecol1:
        # TITLE
        st.header('Project Time Keeper')


    with tittlecol2:
        # BUTTON
        st.button('New Week (clear history)',
                  key='clearall',
                  on_click=btn_click_ClearWork,
                  help='Use with caution.  This will erase all your previous work history!')

    # ------- PROJECTS -----

    column1, column2, column3 = st.columns([4, 5,2])

    with column1:

        # Get project data from the cloud database.
        # df = GetProjectsRandom()
        df = GetProjects_cloud()

        # Add a true/false field to the first column.
        df_df = df.copy()
        st.session_state.df_projects = df_df

        column_config = {'billcode':st.column_config.TextColumn('Billing Code'),
                         'projectname':st.column_config.TextColumn('Project Name')}

        # DATA FRAME
        st.dataframe(st.session_state.df_projects,
                     key='dataframe_projects',
                     hide_index=True,
                     column_config=column_config,
                     column_order=('projectname', 'billcode'),
                     on_select=dataframe_projects_select,
                     selection_mode='single-row')

    with column2:

        st.subheader(st.session_state.active_project_name,
                     help='The project you are working on.')

        # TEXTAREA
        st.text_area('Comments about tasks:',
                     key='txt_comment',
                     on_change=comment_changed,
                     max_chars=200,
                     help='Type a description of the work you are doing.  You can also edit this while working.')

        btndisabled_Delete = (st.session_state.status == 'work') or (st.session_state.active_project_code == '0'
                                                                     )
        st.button('Delete',
                  key='btnDeleteSelected',
                  help='Delete the selected project.',
                  on_click=DeleteSelectedProject,
                  disabled=btndisabled_Delete
                  )
                  #icon=":material/delete:")

        with st.expander('Add a new project and billing',expanded=False):
            instruct = '''
            **Instructions**  
            Enter and ***Submit*** the billing code and the project name below.  They will be added to your database.  
            '''
            st.markdown(instruct)

            # FORM
            with st.form('New Project Information',clear_on_submit=True):
                newcode = st.text_input('Billing Code',key='ti_newcode')
                newname = st.text_input('Name (what you want to call it)',key='ti_newname')

                submitted = st.form_submit_button('Submit',
                                                  disabled=bool(st.session_state.status == 'work'))

                if submitted:
                    if newcode == '' or newname == '':
                        st.warning('Billing Code and Project Name are required.')
                    else:
                        Database_Project_Add(newcode, newname)
                        # Trigger an update of the data editor.

        with st.expander('Bulk upload projects from csv file.',expanded=False):
            instruct = '''
            **Instructions**  
            Your .csv file must have at least the two fields called ***billcode*** and ***projectname***.  
            '''
            st.markdown(instruct)
            st.file_uploader('Bulk Upload Projects',
                             key='btnBulkUpload',
                             help='Upload projects from a .csv file.',
                             type='.csv',
                             on_change=btnBulkUpload_Click)

        # st.button('Go to report page.',
        #           key='btnNavReport',
        #           on_click=btnNavReport_Click)

    with column3:
        with st.container():

           # Control disabled/enabled
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
except:
    ExceptHandler()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/