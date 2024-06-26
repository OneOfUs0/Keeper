import streamlit as st
import pandas as pd
import string, os, random
import datetime
import  traceback, sys

# import firebase_admin
# from firebase_admin import firestore
# from firebase_admin import credentials

from configparser import *

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

def SetStartEndofWeek():
    try:
        today = datetime.date.today()
        daysofweek = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        #                0       1         2            3         4        5          6
        idx = -1 * today.weekday()
        tdelta = datetime.timedelta(days=idx)
        startweek = today + tdelta

        # End
        idx = 6 - today.weekday()
        tdelta = datetime.timedelta(days=idx)
        endweek = today + tdelta

        # save
        st.session_state.startweek = startweek
        st.session_state.endweek = endweek
    except:
        ExceptHandler()

# ================================== INIT  =========================================

if 'reportdf' not in st.session_state:
    st.session_state.reportdf = pd.DataFrame()

if 'startweek' not in st.session_state:
    st.session_state.startweek = datetime.date.today()
    SetStartEndofWeek()
if 'endweek' not in st.session_state:
    st.session_state.endweek = datetime.date.today()
    SetStartEndofWeek()

if 'app_initialized' not in st.session_state:
    st.session_state.app_initialized = False

if 'certfile' not in st.session_state:
    st.session_state.certfile = ''

# do not initialize the app.  This is done on the start page.
if not st.session_state.app_initialized:

    # stop execution
    raise SystemExit(0)
else:
    db = st.session_state.db

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

def ConfigToCSV():
    try:

        inifile = r"C:\GN\Python\Greg_Solutions\keeper\Python38\config_ini.txt"
        outputfile = r'C:\GN\Python\Greg_Solutions\keeper\Python38\projects.txt'

        config = ConfigParser()
        config.read(inifile)

        with open(outputfile, 'w') as fu:

            fu.write('billcode,projectname' + '\n')

            for section in config.sections():
                projectname = section
                billcode = config.get(section, 'number')

                fu.write(billcode + ',' + projectname + '\n')


    except:
        ExceptHandler()

# ===============================  UI  ===========================================

st.header('Report')

col1, col2, col3, col4 = st.columns([2,2,2,2])

with col1:
    subcol1, subcol2 = st.columns([4,4])
    with subcol1:
        st.button('Generate Report',
                  key='btn_report',
                  help='Click to get a summary of the work over the selected dates.',
                  on_click=GenerateTimeReport)
    with subcol2:
        st.page_link('pages/times.py',
                     label='Go Back to Keeping Track of my Time')



with col3:
    st.date_input('Start Date',
                  value=st.session_state.startweek,
                  key='startdate',
                  help='Beginning date to report.')
with col4:
    st.date_input('End Date',
                  value=st.session_state.endweek,
                  key='enddate',
                  help='Ending date to report.')

explain = ''' ****Instructions****  
Select time range and click ***Generate Report***.   This defaults to the current week.   If you select a span of more than one week, the times and projects will aggregate to each day of the week.  
Fill out your timesheet by copying and pasting the billing code, comments, and time into your timesheet.   Time units are hours.
'''
st.markdown(explain)


# Data Frame
report_config = {'Day': st.column_config.TextColumn(label='Day of the Week', width='small'),
                 'Billingcode': st.column_config.TextColumn(label='Billing Code', width='small'),
                 'Time':st.column_config.TextColumn(label='Elapsed Time (hours)',width='small'),
                 'Comments':st.column_config.TextColumn(label='Comments',width='large')}

st.dataframe(st.session_state.reportdf,
             column_config=report_config,
             use_container_width=True)

# st.button('convert config to csv.',
#           on_click=ConfigToCSV)