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

        st.markdown('**Required** setup steps.   This application used Firebase to store your projects information and your work history.')

        PPH1 = '''**Sign into Google and Firebase**  
        First open your web browser and, if you are not yet signed in, sign into your google account. 
        Next search for ***Firebase Console*** and click on the Firebase Console link (http://console.firebase.google.com) . 
        '''

        PPH2 = '''
        **Create a Firebase Project**  
        On the Firebase Console page:      .
        '''

        PPH2_html_outline = '''
        <ol>
        <li>Click on <i>Add project</i>.   Enter the name as <i>TKeeper</i>.</li>
        <li>You can disable the Google Analytics option and click the <i>Create Project</i> button.</li>
        <li>When it is finished, you can click <i>Continue</i></li>
        </ol>
        '''


        PPH3 = '''
        **Create youre Firestore database.**  
        Go to the Goolge Firebase console (http://console.firebase.google.com) and open the ***TKeeper*** project page.  
        '''


        PPH3_html_outline = '''
        <ol>
        <li>On the navigation pane on the left side, open ***Build*** and click on ***Firestore Database***</li>
        <li>Click the <i>Create database</i> button</li>
        <li>Take the default location and click <i>Next</i>.</li>
        <li>Start in <b>production mode</b> and click <i>Create</i>.</li>
        <ol>
        '''

        PPH4 = '''
        ***Create database access certificate***
        '''

        PPH4_html_outline  = '''
        <ol>
        <li>Go to Firebase and selct your new project.</li>
        <li>At Project Overview, click on the "Gear" icon and select "Project Settings".</li>
        <li>Click on the Service "accounts" tab.</li>
        <li>Choose the Python and click on "Generate new private key" button.</li>
        <li>On the Popup click on Generate key".</li>
        <li>Your browser will download a file - open the browser's downloads folder and copy this .json file to C:/firebase.</li>
        <li>Rename the file <i>tkeeper_firebase_cert.json</i></li>
        </ol>
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
    st.markdown(PPH2)

    st.html(PPH2_html_outline)


    # CREATE THE CERTIFICATE TO CONNECT TO YOUR PROJECTS DATABASE.
    st.markdown(PPH3)
    st.html(PPH3_html_outline)

    st.markdown(PPH4)
    st.html(PPH4_html_outline)

except:
    ExceptHandler()


