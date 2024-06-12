import streamlit as st
import random
import pandas as pd
import string
import datetime
import  traceback, sys

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

def ExceptHandler():
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    print(pymsg)


st.set_page_config(page_title='Report Times',
                   layout="wide",
                   page_icon=':stopwatch:',
                   menu_items={
                       'Report a Bug':'https://www.google.com/appserve/security-bugs/m2/new',
                       'Get Help':'https://somafm.com/dronezone',
                       'About':'Created by Greg Nichols'
                   })

# ================================== INIT  =========================================

if 'reportdf' not in st.session_state:
    st.session_state.reportdf = pd.DataFrame()

if 'app_initialized' not in st.session_state:
    st.session_state.app_initialized = False

# THIS IS TO ALLOW ONLY ME TO ACCESS SINCE I HAVE THE CREDENTIALS CERTIFICATE.
cred = credentials.Certificate(r'C:\Users\36352\PycharmProjects\Keeper\tkeeper-c0270-firebase-adminsdk-ou3gc-03d4e1ddde.json')

if not st.session_state.app_initialized:
    app = firebase_admin.initialize_app(cred)
    st.session_state.app_initialized = True

db = firestore.client()

# ================================== FUNCTIONS =========================================

def GetWorkRecords():
    try:

        start_ord = st.session_state.startdate.toordinal()
        end_ord = st.session_state.enddate.toordinal()


        # Get records from the database.
        #docs = db.collection('worklog').get()
        docs = db.collection('worklog').where('date_ord','>=',start_ord).where('date_ord','<=',end_ord).get()
        dbrecords = []
        for doc in docs:
            rec = doc.to_dict()
            dbrecords.append(rec)

        # Parse out and sumarize
        Totals = {}

        for rec in dbrecords:
            day = rec['aday']
            etime = rec['elapsedtime']
            billcode = rec['billcode']
            comment = rec['comment']

            if day not in Totals:
                    Totals[day] = {}

            if billcode not in Totals[day]:
                Totals[day][billcode] = {}
                Totals[day][billcode]['Time'] = float(0.0)
                Totals[day][billcode]['comment'] = ''

            Totals[day][billcode]['Time'] += float(etime)
            coms = Totals[day][billcode]['comment']
            Totals[day][billcode]['comment'] = coms + '  ' + comment

        # rearrange as a list of dicts.
        records = []
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']:
            if day in Totals:
                for billcode in Totals[day]:
                    time = Totals[day][billcode]['Time']
                    comments = Totals[day][billcode]['comment']
                    rec = {'Day':day,'Billingcode':billcode,'Time':time,'Comments':comments}
                    records.append(rec)


        return records
    except:
        ExceptHandler()


def CreateRandomRecords():
    try:

        fields = ['day', 'date', 'billcode', 'projectname', 'hours', 'comments']
        records = []

        for i in range(0, 10):
            code = ''
            for cc in range(0, 4):
                for c in range(0, 3):
                    code += str(random.randint(2, 99))
                code += '.'

            name = ''
            for x in range(0, 25):
                name += list(string.ascii_lowercase)[random.randint(0, 23)]

            comments = ''
            for x in range(0, 25):
                comments += list(string.ascii_lowercase)[random.randint(0, 23)]
            day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'][random.randint(0, 4)]

            date = '06/01/2024'

            rec = {'day': day, 'date': date, 'billcode': code.strip('.'), 'projectname': name, 'comments': comments}

            records.append(rec)

        return records
    except:
        ExceptHandler()

# ================================== CALLBACKS =========================================
def GenerateTimeReport():
    try:
        #records = CreateRandomRecords()
        records = GetWorkRecords()

        df = pd.DataFrame(records)

        st.session_state.reportdf = df

    except:
        ExceptHandler()

# ===============================  UI  ===========================================

st.header('Report')

col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.button('Generate Report',
              key='btn_report',
              on_click=GenerateTimeReport)
with col2:
    st.date_input('Start Date',
                  key='startdate')
with col3:
    st.date_input('End Date',
                  key='enddate')


# create the Data Frame
st.dataframe(st.session_state.reportdf,
             use_container_width=True)