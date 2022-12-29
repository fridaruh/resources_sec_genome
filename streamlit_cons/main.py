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
spreadsheetname = "Database"


#worksheet = sh.get_worksheet(spreadsheetname)
####

worksheet_list = sh.worksheets()
st.write(worksheet_list)

# Functions 
#@st.cache()
# Get our worksheet names
#def worksheet_names():
#    sheet_names = []   
#    for sheet in worksheet_list:
#        sheet_names.append(sheet.title)  
#    return sheet_names

# Get the sheet as dataframe
#def load_the_spreadsheet(spreadsheetname):
#    worksheet = sh.worksheet(spreadsheetname)
#    df = DataFrame(worksheet.get_all_records())
#    return df

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
show = st.sidebar.button('Mostrar información OpenAI')
if show:
    what = "Get very short abstract in spanish of this text: "+summary
    why = 'Answer very shortly in spanish why is important this text: '+summary
    resumen_openai_what = openai_connect().openai.Completion.create(model="text-davinci-003", prompt=what, temperature=0, max_tokens=100)
    resumen_openai_why = openai_connect().openai.Completion.create(model="text-davinci-003", prompt=why, temperature=0, max_tokens=100)

    st.write('¿Sobre qué trata el texto?')
    st.write(resumen_openai_what['choices'][0]['text'])
    st.write('¿Por qué es importante?')
    st.write(resumen_openai_why['choices'][0]['text'])
else:
    st.write('No se ha mostrado la información')

#Agregar entrada de información
add = st.sidebar.checkbox('Agregar señal')
if add :  
    link_nuevo = st.sidebar.text_input('link_nuevo')
    confirm_input = st.sidebar.button('Confirm')
    
    if confirm_input:
        now = datetime.now()
        opt = {'Enlace': [link_nuevo],
                'Resumen' : [summary],
              'Time_stamp' :  [now],
              'What?' : [resumen_openai_what['choices'][0]['text']],
                'So what?' : [resumen_openai_why['choices'][0]['text']]}
        opt_df = DataFrame(opt)
        df = load_the_spreadsheet('Hoja 1')
        new_df = df.append(opt_df,ignore_index=True)
  
