import streamlit as st
import  traceback, sys, json,uuid
from io import StringIO

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials


def ExceptHandler():
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    print(pymsg)

try:
    st.set_page_config(page_title='Setup',
                       layout="wide",
                       page_icon=':stopwatch:',
                       menu_items={'About': 'Created by OneOfUs0, June 2024',
                                   'Get Help': 'https://somafm.com/dronezone/'},
                       initial_sidebar_state = "collapsed"
                       )

    if 'app_initialized' not in st.session_state:
        st.session_state.app_initialized = False
    if 'certfile' not in st.session_state:
        st.session_state.certfile = ''

    # HACK
    # This will disable the sidebar navigation.
    # st.markdown("""
    #     <style>
    #         section[data-testid="stSidebar"][aria-expanded="true"]{
    #             display: none;
    #         }
    #     </style>
    #     """, unsafe_allow_html=True)

    def btnUploadCert_Change():
        try:
            print('------- initialize with cert file ---------')
            thefile = st.session_state.btnUploadCert

            if thefile is not None:

                # convert the UploadedFile to a dict.
                stringio = StringIO(thefile.getvalue().decode("utf-8"))
                cert_dict = json.load(stringio)

                if st.session_state.app_initialized:
                    print('Database connection is already initialized.')
                    st.warning('Database connection is already initialized.  You cannot change this one or create a second one.')
                else:
                    try:
                        appname = str(uuid.uuid1())
                        st.session_state.appname = appname

                        cred = credentials.Certificate(cert_dict)
                        app = firebase_admin.initialize_app(cred,name=appname)
                        db = firestore.client(app)

                        st.session_state.app_initialized = True
                        st.session_state.certfile = thefile
                        st.session_state.db = db
                        st.success('Succeeded connecting to the database.  You may continue.' + '\n' + '   (Your Firebase App name is ' + appname + ')')
                    except:
                        st.session_state.app_initialized = False

                        tb = sys.exc_info()[2]
                        tbinfo = traceback.format_tb(tb)[0]
                        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])

                        st.warning('Database connection failed.' + '\n' + pymsg)

                        ExceptHandler()
        except:
            ExceptHandler()


    if st.session_state.app_initialized:
        st.header('Database connection established')

        st.page_link('pages/times.py',
                     label='Click Here to Start Keeping Track of Time')


    if not st.session_state.app_initialized:
        st.header('Start Here')
        st.subheader('Upload Certificate file')
        st.markdown('If you have already created a data access certificate file, upload it below.  If you have not  '
                    'yet created the file, follow the ***Setup Steps*** to create one.')
        st.file_uploader('Upload the certificate json file here.',
                         key='btnUploadCert',
                         help='Upload the certificate file you created with Firestore.',
                         type='.json',
                         on_change=btnUploadCert_Change)



        with st.container():

            st.header('Setup Steps')
            #st.subheader('Setup Required ')

            st.markdown('This application uses a cloud database called ***Firestore***, part of Google\'s ***Firebase***, '
                        'to store your project\'s information and your work history.   You will need to use your Google '
                        'account to create this database "container" and grant access to this application.  '  
                        'Follow the three steps below.')

            PPH1 = '''**Sign into Google and Firebase**  
            First open your web browser and, if you are not yet signed in, sign into your Google account.  
            
            '''

            PPH2 = '''
            **Create a Project in Firebase**  
            Go to the Firebase Console page http://console.firebase.google.com.
            '''

            PPH2_html_outline = '''
            <ol>
            <li>Click on <b><i>Add project</i></b>.   Enter the name as <b><i>TKeeper</i></b>.</li>
            <li>You can disable the Google Analytics option and click the <b><i>Create Project</i></b> button.</li>
            <li>When it is finished, click<b> <i>Continue.</i></b></li>
            </ol>
            '''


            PPH3 = '''
            **Create a Database in Firestore**  
            Go to the Goolge Firebase console: http://console.firebase.google.com and open the ***TKeeper*** project page.  
            '''


            PPH3_html_outline = '''
            <ol>
            <li>On the navigation pane on the left side, open <b><i>Build</i></b> and click on <b><i>Firestore Database.</i></b></li>
            <li>Click the <b><i>Create database.</i></b> button</li>
            <li>Take the default location and click <b><i>Next</i></b>.</li>
            <li>Start in <b>production mode</b> and click <b><i>Create</i></b>.</li>
            <ol>
            '''

            PPH4 = '''
            **Create a Database Access Certificate**  
            Go to the Goolge Firebase console http://console.firebase.google.com and open the ***TKeeper*** project page.
            '''

            PPH4_html_outline  = '''
            <ol>
            <li>At Project Overview, click on the <b>Gear</b> icon and select <b><i>Project Settings</b></i>.</li>
            <li>Click on the <b><i>Service accounts</b></i> tab.</li>
            <li>Choose the Python and click on <b><i>Generate new private key</b></i> button.</li>
            <li>On the Popup, click on <b><i>Generate key</b></i>.</li>
            <li>Your browser will download a file - open the browser's downloads folder and copy this .json file to a place that you will remember.</li>
            <li>You may want to give this file a simple name like <i>tkeeper_firebase_cert.json.</i></li>
            </ol>
            <a href="https://clemfournier.medium.com/how-to-get-my-firebase-service-account-key-file-f0ec97a21620">Addtional Help Creating the Certificate</a>
            '''


            # CREATE FIREBASE ACCOUNT
            with st.container():
                col1, col2 = st.columns([5,3])
                with col1:
                    st.markdown(PPH1)

                with col2:

                    with st.expander('Video for using Firebase and Firestore',expanded=False):

                        # video
                        url = r'https://www.youtube.com/watch?v=3B1b-RU1BeU'
                        st.video(url)


        # CREATE THE PROJECT
        st.subheader('1. Create Project')
        st.markdown(PPH2)

        st.html(PPH2_html_outline)


        # CREATE THE CERTIFICATE TO CONNECT TO YOUR PROJECTS DATABASE.
        st.subheader('2. Create Database')
        st.markdown(PPH3)
        st.html(PPH3_html_outline)

        st.subheader('3. Create Certificate')
        st.markdown(PPH4)
        st.html(PPH4_html_outline)

        # put some notes about the collections and documents that this application will put here.
        # Warn not to change these or add to the collections.

except:
    ExceptHandler()


