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

table_md = f'''
    |Script/Language|Hindi|Urdu|
    |--|--|--|
    |DevaNāgarī|**{outputs['hi']}**|{outputs['u2h']}|
    |PersoArabic|{outputs['h2u']}|**{outputs['ur']}**|
    |Roman (Approx)|{outputs['h2e']}|{outputs['u2e']}|
    '''
col2.markdown(table_md)
