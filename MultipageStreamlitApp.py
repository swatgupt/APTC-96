import home
import streamlit as st
import data
import plots
import predict
import numpy as np
import pandas as pd


st.set_page_config(page_title = 'Car Price Prediction',
                    page_icon = ':car:',
                    layout = 'centered',
                    initial_sidebar_state = 'auto'
                    )

words_dict = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "eight": 8, "twelve": 12}
def num_map(series):
    return series.map(words_dict)

@st.cache()
def load_data():
    cars_df = pd.read_csv("car-prices.csv")
    car_companies = pd.Series([car.split(" ")[0] for car in cars_df['CarName']], index = cars_df.index)
    cars_df['car_company'] = car_companies
    cars_df.loc[(cars_df['car_company'] == "vw") | (cars_df['car_company'] == "vokswagen"), 'car_company'] = 'volkswagen'
    cars_df.loc[cars_df['car_company'] == "porcshce", 'car_company'] = 'porsche'
    cars_df.loc[cars_df['car_company'] == "toyouta", 'car_company'] = 'toyota'
    cars_df.loc[cars_df['car_company'] == "Nissan", 'car_company'] = 'nissan'
    cars_df.loc[cars_df['car_company'] == "maxda", 'car_company'] = 'mazda'
    cars_df.drop(columns= ['CarName'], axis = 1, inplace = True)
    cars_numeric_df = cars_df.select_dtypes(include = ['int64', 'float64']) 
    cars_numeric_df.drop(columns = ['car_ID'], axis = 1, inplace = True)
    cars_df[['cylindernumber', 'doornumber']] = cars_df[['cylindernumber', 'doornumber']].apply(num_map, axis = 1)
    car_body_dummies = pd.get_dummies(cars_df['carbody'], dtype = int)
    car_body_new_dummies = pd.get_dummies(cars_df['carbody'], drop_first = True, dtype = int)
    cars_categorical_df = cars_df.select_dtypes(include = ['object'])
    cars_dummies_df = pd.get_dummies(cars_categorical_df, drop_first = True, dtype = int)
    cars_df.drop(list(cars_categorical_df.columns), axis = 1, inplace = True)
    cars_df = pd.concat([cars_df, cars_dummies_df], axis = 1)
    cars_df.drop('car_ID', axis = 1, inplace = True)
    final_columns = ['carwidth', 'enginesize', 'horsepower', 'drivewheel_fwd', 'car_company_buick', 'price']
    return cars_df[final_columns]
  
final_cars_df = load_data()

pages_dict = {
                "Home": home,
                "View Data": data, 
                "Visualise Data": plots, 
                "Predict": predict
            }

st.sidebar.title('Navigation')
user_choice = st.sidebar.radio("Go to", tuple(pages_dict.keys()))
if user_choice == "Home":
    home.app() # The 'app()' function should not take any input if the selection option is "Home".
else:
    selected_page = pages_dict[user_choice]
    selected_page.app(final_cars_df) 

def app():
	st.header("Car Price Prediction App")
	st.text("""
            This web app allows a user to predict the prices of a car based on their 
            engine size, horse power, dimensions and the drive wheel type parameters.
        	""")

def app(car_df):
    st.header("View Data")
    with st.beta_expander("View Dataset"):
        st.table(car_df)
    st.subheader("Columns Description:")
    if st.checkbox("Show summary"):
        st.table(car_df.describe())  
    beta_col1, beta_col2, beta_col3 = st.beta_columns(3)

    with beta_col1:
        if st.checkbox("Show all column names"):
            st.table(list(car_df.columns))
    with beta_col2: 
        if st.checkbox("View column data-type"):
            st.table(car_df.dtypes)
    with beta_col3:
        if st.checkbox("View column data"):
            column_data = st.selectbox('Select column', tuple(car_df.columns))
            st.write(car_df[column_data])

