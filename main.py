
import streamlit as st
import random
import pandas as pd
import string
import datetime

# -------------------- development notes --------------------
#  To run this from Pycharm, do this:
#   1. open in PyCharm - (already here)
#  2.  go to the Terminal and cd to this folder.
#  3. type "streamlit run main.py"
#  4. on the app, set setting to "Run on Save"
#
# ---------------------------------------------------------

# ================================== INIT  =========================================

st.set_page_config(page_title='Time Keeper Controls',page_icon=':stopwatch:',
                   menu_items={'About':'Created by Greg Nichols',
                               'Get Help':'https://somafm.com/dronezone/'})

# initialize
if 'status' not in st.session_state:
    st.session_state.status = 'You are not working'
    print('----> init status')
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

def AddNewProject(newcode, newname):
    print('code is ' + newcode + ' for new projet ' + newname)

    # write the new code and project to the dataframe.
    rec = {'code': newcode.strip('.'), 'name': newname}

def AddEntry():
    # LOG billcode, time, and comments.

    start = st.session_state.starttime
    stop = st.session_state.stoptime

    # elapsed = stop - start
    # elap_seconds = elapsed.total_seconds()
    # print('Worked for ' + str(int(elap_seconds)) + ' seconds on ' + st.session_state.comment)

    # write this to the work log.

def startworking():
    print('START WORKING!')

    # status change
    #st.session_state.startstop_text = 'Toggle to stop working'
    # start time
    st.session_state.starttime = datetime.datetime.now()
    print('Started timer')

def stopworking():
    print('STOPPED WORKING')

    actcode = st.session_state.active_project_code


    # status change
    #st.session_state.startstop_text = 'Toggle to start working'

    # stop time
    st.session_state.stoptime = datetime.datetime.now()
    print('Stopped timer at ' + str(st.session_state.stoptime) + ' CODE: ' + actcode)

    # LOG billcode, time, and comments.
    AddEntry()



# ================================== CALLBACKS =========================================

def startstop_onclick(status):
    pass

    # if status == 'working':
    #     print('STOPPING WORK')
    #
    #     # status change
    #     st.session_state.status = 'resting'
    #
    #     # stop time
    #     st.session_state.stoptime = datetime.datetime.now()
    #     print('Stopped timer at ' + str(st.session_state.stoptime) )
    #
    #     # button text
    #     st.session_state.startstop_text = 'Start'
    #
    #     # LOG
    #     AddEntry()
    #
    # if status == 'resting':
    #     print('STARTING WORK')
    #
    #     # status change
    #     st.session_state.status = 'working'
    #
    #     # start time
    #     st.session_state.starttime = datetime.datetime.now()
    #     print('Started timer')
    #
    #
    #     # button text
    #     st.session_state.startstop_text = 'Stop'

def comment_changed():

    thecomment = st.session_state.txt_comment
    st.session_state.comment = thecomment
    print('updated to ' + thecomment)

def data_editor_changed():
    print('NEW SELECTION')


# ===============================  UI  ===========================================

st.title('Project Time Keeper')

st.divider()

# ------- CONTROLS - StartStop, Comments -----
st.subheader('Control work here.') #st.session_state.status)

#st.button(st.session_state.startstop_text,key='btn_startstop',on_click=startstop_onclick(st.session_state.status))

type(st.session_state['active_project_code'])


onoff = st.toggle('Working',key='toggle_work',
                  disabled=False,
                  help='Turn on when you start working.  Turn off when you stop working.')
if onoff:
    startworking()
else:
    stopworking()

st.text_area('Comments',key='txt_comment', on_change=comment_changed(), max_chars=200,help='Type comments for this work.')


# ------- PROJECTS -----
st.subheader('Projects',help='Choose the project you will be working on.')

#st.dataframe(GetProjects(),use_container_width=True)

# get pandas dataframe
df = GetProjects()


# Add a true/false field to the first column.
df_selections = df.copy()
df_selections.insert(0, "Apply to this", False)

# configure the "Apply to this" column to have checkboxes
column_config = {'Apply to this':st.column_config.CheckboxColumn(required=True)}

# create the Data Editor
edited_df = st.data_editor(df_selections,
                           hide_index=True,
                           column_config=column_config,
                           disabled=['code','name'],  use_container_width=True,
                           on_change=data_editor_changed()
                           )

# check for mulitple selections.
sel_codes = edited_df.loc[edited_df['Apply to this']]["code"]
if len(sel_codes) == 0:
    st.session_state.active_project_code = '0'
elif len(sel_codes) > 1:
    st.warning('Select only one Project.')
    st.session_state.active_project_code = '0'
else:
    selected_code = sel_codes.iloc[0]
    # save to session
    st.session_state.active_project_code=selected_code


# ------- NEW PROJECT -----
with st.form('New Project Information',clear_on_submit=True):
    st.subheader("Add a New Project")
    newcode = st.text_input('Billing Code',key='ti_newcode')
    newname = st.text_input('Name (what you want to call it)',key='ti_newname')
    submitted = st.form_submit_button('Submit')
    if submitted:
        if newcode == '' or newname == '':
            st.warning('code and name are required.')
        else:
            AddNewProject(newcode,newname)


# ===============================  MAIN  ===========================================

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print('---- MAIN ----')



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
