# S1.1: Design the Page 1 of the multipage app.
# Import necessary modules
import numpy as np
import pandas as pd
import streamlit as st

# Define a function 'app()' which accepts 'car_df' as an input.
def app(car_df):
    st.header("View Data")
    # Add an expander and display the dataset as a static table within the expander.
    with st.beta_expander("View Dataset"):
        st.table(car_df)

    st.subheader("Columns Description:")
    beta_col1, beta_col2 = st.beta_columns(2)

    # Add a checkbox in first column. Display the column names of 'car_df' on the click of checkbox.
    with beta_col1:
        if st.checkbox("Show all column names"):
            st.table(list(car_df.columns))

    # Add a checkbox in second column. 
    # On the click of the checkbox, add a selectbox which accepts the column name whose data needs to be displayed.
    with beta_col2:
        if st.checkbox("View column data"):
            column_data = st.selectbox('Select column', ('enginesize', 'horsepower', 'carwidth', 'drivewheel', 'price'))
            if column_data == 'drivewheel':
                st.write(car_df['drivewheel'])
            elif column_data == 'carwidth':
                st.write(car_df['carwidth'])
            elif column_data == 'enginesize':
                st.write(car_df['enginesize'])
            elif column_data == 'horsepower':
                st.write(car_df['horsepower'])
            else:
                st.write(car_df['price'])

    if st.checkbox("Show summary"):
        st.table(car_df.describe())