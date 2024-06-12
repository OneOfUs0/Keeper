import streamlit as st
import  traceback, sys


def ExceptHandler():
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    print(pymsg)

try:
    st.set_page_config(page_title='Setup',
                       layout="wide",
                       page_icon=':stopwatch:'
                       # menu_items={
                       #     'Report a Bug':'https://www.google.com/appserve/security-bugs/m2/new',
                       #     'Get Help':'https://somafm.com/dronezone',
                       #     'About':'Created by Greg Nichols'}
                       )

    with st.container():

        st.header('Setup Required ')
        #st.subheader('Setup Required ')

        st.markdown('**Required** setup steps.   This application uses Firebase to store your project\'s information and your work history.')

        PPH1 = '''**Sign into Google and Firebase**  
        First open your web browser and, if you are not yet signed in, sign into your google account. 
        Next search for ***Firebase Console*** and click on the Firebase Console link (http://console.firebase.google.com) . 
        '''

        PPH2 = '''
        **Create a Project in Firebase**  
        Go to the Firebase Console page (http://console.firebase.google.com).
        '''

        PPH2_html_outline = '''
        <ol>
        <li>Click on <b><i>Add project</i></b>.   Enter the name as <b><i>TKeeper</i></b>.</li>
        <li>You can disable the Google Analytics option and click the <b><i>Create Project</i></b> button.</li>
        <li>When it is finished, you can click<b> <i>Continue</i></b></li>
        </ol>
        '''


        PPH3 = '''
        **Create a Database in Firestore**  
        Go to the Goolge Firebase console (http://console.firebase.google.com) and open the ***TKeeper*** project page.  
        '''


        PPH3_html_outline = '''
        <ol>
        <li>On the navigation pane on the left side, open <b><i>Build</i></b> and click on <b><i>Firestore Database</i></b></li>
        <li>Click the <b><i>Create database</i></b> button</li>
        <li>Take the default location and click <b><i>Next</i></b>.</li>
        <li>Start in <b>production mode</b> and click <b><i>Create</i></b>.</li>
        <ol>
        '''

        PPH4 = '''
        ***Create a Database Access Certificate***  
        Go to the Goolge Firebase console (http://console.firebase.google.com) and open the ***TKeeper*** project page.
        '''

        PPH4_html_outline  = '''
        <ol>
        <li>At Project Overview, click on the <b>Gear</b> icon and select <b><i>Project Settings</b></i>.</li>
        <li>Click on the <b><i>Service accounts</b></i> tab.</li>
        <li>Choose the Python and click on <b><i>Generate new private key</b></i> button.</li>
        <li>On the Popup, click on <b><i>Generate key</b></i>.</li>
        <li>Your browser will download a file - open the browser's downloads folder and copy this .json file to <i>C:/firebase</i>.</li>
        <li>Rename the file <i>tkeeper_firebase_cert.json</i></li>
        </ol>
        <a href="https://clemfournier.medium.com/how-to-get-my-firebase-service-account-key-file-f0ec97a21620">Addtional Help Creating the Certificate</a>
        '''


        # CREATE FIREBASE ACCOUNT
        with st.container():
            col1, col2 = st.columns([5,3])
            with col1:
                st.markdown(PPH1)

            with col2:

                with st.expander('Video for creating an account:',expanded=False):

                    # video for creating and account.
                    url = r'https://www.youtube.com/watch?v=3B1b-RU1BeU'
                    st.video(url)


    # CREATE THE PROJECT
    st.subheader('Create Project')
    st.markdown(PPH2)

    st.html(PPH2_html_outline)


    # CREATE THE CERTIFICATE TO CONNECT TO YOUR PROJECTS DATABASE.
    st.subheader('Create Database')
    st.markdown(PPH3)
    st.html(PPH3_html_outline)

    st.subheader('Create Certificate')
    st.markdown(PPH4)
    st.html(PPH4_html_outline)

    # put some notes about the collections and documents that this application will put here.
    # Warn not to change these or add to the collections.

except:
    ExceptHandler()


