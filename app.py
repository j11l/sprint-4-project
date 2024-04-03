import streamlit as st
import pandas as pd
import plotly.express as px

# read in csv data for dataframe + make relevant edits
vehicles = pd.read_csv('./vehicles_us.csv')

def getmake(makemodel):
    '''Get the first word from a string combining make and model.'''
    make = makemodel.split(' ',1)[0]
    return make

def hyphenate_trucks(model):
    '''If input string contains unhyphenated Ford model name, replace with hyphenated version'''
    model = model.replace('f150','f-150')
    model = model.replace('f250','f-250')
    model = model.replace('f350','f-350')
    return model

# clean unhyphenated ford truck model names from data
vehicles['model'] = vehicles['model'].apply(hyphenate_trucks)

# specify models of interest (pickup trucks only)
pickup_models = ['ford f-150', 'ford f-250', 'ford f-350', 'ford ranger', 'toyota tacoma', 'toyota tundra', \
                 'chevrolet colorado', 'chevrolet silverado', 'ram 1500', 'ram 2500', 'ram 3500', 'gmc sierra', \
                 'nissan frontier', 'dodge dakota']

# filter dataframe to rows where 'model' contains a string from list of known pickup_models
# https://stackoverflow.com/questions/61158898/filter-pandas-where-some-columns-contain-any-of-the-words-in-a-list
pickups = vehicles[vehicles['model'].str.contains('|'.join(pickup_models))]

# add 'make' column to simplify comparisons by make
pickups['make'] = pickups['model'].apply(getmake)



### BEGIN STREAMLIT PART ###
st.header('Do some pickup makes sell faster or for more money?')

st.write("Using data from approximately a year of used car advertisements, I created this scatter \
          plot to compare advertised prices and number of days listed for various makes of pickup \
          truck; it might be useful to know if some makes tend to sell faster, or for a higher \
          price. You can click on the legend to show or hide different makes.")

# this is the scatter plot
scatterfig = px.scatter(pickups, x='days_listed', y='price', color='make',hover_data=['model','condition','odometer'],labels={'days_listed':'Days Listed','price':'Price'},title='Pickup Prices and Days Listed, by Make')
st.plotly_chart(scatterfig)

st.write("Caveat: there may be cases where the same vehicle appears in the data more than once. See \
          the line of points at $189,000 where Ford trucks with identical odometer readings appear \
          to have been listed for different numbers of days.")

st.write("Let's look at price distributions for three of the most popular makes.")

# histogram: prices across 3 major makes
big3price = pickups.query("make in ['ford', 'chevrolet', 'ram']")[['price','make']]
big3price_hist = px.histogram(big3price, x="price", color="make", barmode="overlay",title="Price Frequencies by Make")
big3price_hist.update_layout(yaxis_title_text = 'Number of Trucks Advertised',xaxis_title_text = 'Price')
st.plotly_chart(big3price_hist)

# This is the checkbox. It doesn't work, but please review the rest of my code while I figure this out
hist1check = st.checkbox("Cut off at 100,000", value=False)

st.write("The median price for Chevrolet trucks appears to be a little higher than it is for Ford. \
          There are fewer Ram truck advertisements in our dataset, but the median sale price for \
          these is even higher.")

st.write("Now let's do a similar comparison for days listed. There are several factors which may \
          affect how long a car may stay on the lot, including the fairness of its price, but \
          here I'm generally interested in how quickly a typical truck will be sold.")

# histogram: days listed across 3 major makes
big3days = pickups.query("make in ['ford', 'chevrolet', 'ram']")[['days_listed','make']]
big3days_hist = px.histogram(big3days, x="days_listed", color="make", barmode="overlay",title="Listing Length Frequencies by Make")
big3days_hist.update_layout(yaxis_title_text = 'Number of Trucks Advertised',xaxis_title_text = 'Days Listed')
st.plotly_chart(big3days_hist)

st.write("It appears that there isn't a substantial difference in how long a typical truck is \
          advertised for sale between the three makes. Distributions vary a little, but the \
          means are fairly similar.")