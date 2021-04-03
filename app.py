import streamlit as st
import pandas as pd

st.title('My first app')

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

text = st.text_area(
    "Your text",
    "I dreamed a dream."
)

if not text:
    text = "Emptiness"

st.write(text+"555")
