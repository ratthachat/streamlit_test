import streamlit as st
import pandas as pd
from googletrans import Translator
translator = Translator()

st.title('Streamlit Lingo Bot')
col1, col2 = st.beta_columns(2)

text = col1.text_area(
    "Your text",
    "I dreamed a dream."
)

if not text:
    text = "Emptiness"

col1.write(text+"555")

# outputs={

xx = 'hey'
yy = 102

table_md = f'''
    |Script/Language|Eng|Lang|
    |--|--|--|
    |Conversation|**{xx}**|{yy}|
    |Bot Latest|{xx}|**{yy}**|
    |You say|{xx}|{yy}|
    '''
    
col2.markdown(table_md)
