# Streamlit-Google Sheet
## Modules
import streamlit as st 
from pandas import DataFrame
from google.oauth2 import service_account
from gsheetsdb import connect
import os
import openai
import gspread
from gspread_pandas import Spread
from gspread_pandas import Client
from google.oauth2 import service_account

from datetime import datetime

# Disable certificate verification (Not necessary always)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#Connect to openAI
def openai_connect():
    credential_openai= st.secrets["openai_creds"]
    openai.api_key = credential_openai.openai_api_key
    return openai


# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

gc = gspread.authorize(credentials)

sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1pt5tV_zFIIGQgJ-kN88LhkiieuHSLUodSzQ4Dyfjido/edit?usp=sharing')
worksheet_list = sh.worksheets()

spreadsheetname= worksheet_list[0].title

# Create a Google Authentication connection object


cliente = Client(scope="https://www.googleapis.com/auth/spreadsheets",creds=credentials)

#Revisar esto, quizá deba hardcodearse

spreadsheetnames = "Database"
spread = Spread(spreadsheetnames,client = cliente)


# Functions 
@st.cache()
# Get our worksheet names
def worksheet_names():
    sheet_names = []   
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)  
    return sheet_names

worksheet = sh.worksheet(spreadsheetname)

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
   worksheet = sh.worksheet(spreadsheetname)
   df = DataFrame(worksheet.get_all_records())
   return df


def update_the_spreadsheet(spreadsheetnames,dataframe):
    col = ['Enlace','Resumen','Time_stamp','What?','So what?']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetnames,index = False)
    st.info('Updated to GoogleSheet')


st.header('Streamlit: Banco de Señales')

st.title('Información de la señal')
# Introducir el enlace
st.write('Introduce the link')
link = st.text_input('Link')

# Introducir el resumen
st.write('Introduce el resumen')
summary = st.text_input('Summary')


# Mostrar la información
st.title('Mostrar la información')
show = st.button('Mostrar información OpenAI')

what = "Get very short abstract in spanish of this text: "+summary
why = 'Answer very shortly in spanish why is important this text: '+summary
resumen_openai_what = openai_connect().Completion.create(model="text-davinci-003", prompt=what, temperature=0, max_tokens=100)
resumen_openai_why = openai_connect().Completion.create(model="text-davinci-003", prompt=why, temperature=0, max_tokens=100)

resumen_openai_what_ans = resumen_openai_what['choices'][0]['text']
resumen_openai_why_ans = resumen_openai_why['choices'][0]['text']

if show:
    st.write('¿Sobre qué trata el texto?')
    st.write(resumen_openai_what_ans)
    st.write('¿Por qué es importante?')
    st.write(resumen_openai_why_ans)
else:
    st.write('No se ha mostrado la información')


#Agregar entrada de información

confirm_input = st.button('Confirm')
if confirm_input:
    now = datetime.now()
    opt = {'Enlace': [link],
            'Resumen' : [summary],
            'Time_stamp' : [now],
            'What?' : [resumen_openai_what_ans],
            'So what?' : [resumen_openai_why_ans]}
    opt_df = DataFrame(opt)
    df = load_the_spreadsheet(spreadsheetname)
    df = DataFrame(df)
    new_df = df.append(opt_df,ignore_index=True)
    update_the_spreadsheet(spreadsheetnames,new_df)
else: 
    st.write('No se ha confirmado la entrada')
