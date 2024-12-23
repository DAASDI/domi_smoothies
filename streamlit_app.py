# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Example Streamlit App :balloon:")
st.write(
    """Choose your fruits you want in your custom smoothie
    """)

#import streamlit as st

name_on_order = st.text_input('Name of smoothie : ')
st.write('The name of the smoothie will be ', name_on_order)

#option = st.selectbox(
#    'What is your favorite fruit ?',
#    ("Banana", "Strawberries", "Peache"))
#st.write("Your favorite fruit is :", option)

#from snowflake.snowpark.functions import col
cnx = st.connection('snowflake')
session = cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)
ingredients_string = '';
if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + '    '
    #st.write(ingredients_string)
    st.subheader(fruit_chosen + ' Nuutrition information')
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruit_chosen)
    sd_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

time_to_insert = st.button('Submit Order')

if time_to_insert:
    import requests
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
    sd_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    st.success('Your Smoothie is ordered!',  icon="✅")
