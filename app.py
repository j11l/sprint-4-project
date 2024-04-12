import streamlit as st
import pandas as pd
import plotly.express as px

###
### Data processing
### For a full explanation of my data processing strategy, see notebooks/EDA.ipynb.
###

# Read in CSV data for dataframe + clean up.
vehicles = pd.read_csv('./vehicles_us.csv',parse_dates=['date_posted'])
# Remove probable inaccurate prices from dataset.
vehicles = vehicles[vehicles['price'] >= 500]
# Correct model years for three particular vehicles where it's definitely wrong.
vehicles.loc[[33906, 33907, 22595],'model_year'] = 2008, 2008, 1958

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

# Correct unhyphenated Ford truck model names.
vehicles['model'] = vehicles['model'].apply(hyphenate_trucks)

# Get median model year, based on model, for vehicles missing it.
model_median_year = vehicles.query('model_year.isna()')['model'].drop_duplicates().to_frame()
def get_median_year(m):
    '''Return median model year for a given model in vehicles dataframe.'''
    return vehicles.query('model == @m')['model_year'].median()
model_median_year['median_year'] =  model_median_year['model'].apply(get_median_year)
model_median_year = model_median_year.set_index('model').median_year
vehicles['model_year'] = vehicles['model_year'].fillna(vehicles['model'].map(model_median_year))

# Get likely number of cylinders, based on model, for vehicles missing it
model_median_cylinders = vehicles.query('cylinders.isna()')['model'].drop_duplicates().to_frame()
def get_median_cylinders(m):
    '''Return median cylinder value for a given model in vehicles dataframe.'''
    return vehicles.query('model == @m')['cylinders'].median()
model_median_cylinders['median_cylinders'] = model_median_cylinders['model'].apply(get_median_cylinders)
model_median_cylinders = model_median_cylinders.set_index('model').median_cylinders
vehicles['cylinders'] = vehicles['cylinders'].fillna(vehicles['model'].map(model_median_cylinders))

# Get median odometer value, based on model year, for vehicles missing it.
myear_med_odo = vehicles.query('odometer.isna()')['model_year'].drop_duplicates().to_frame()
def get_median_odo(my):
    '''Return median odometer value for a given model year in vehicles dataframe.'''
    median_odo = vehicles.query('model_year == @my')['odometer'].median()
    # catch the one case where median_odo is NaN because there are no other cars in model year; return 0
    if median_odo == median_odo:
        return median_odo
    else:
        return 0
myear_med_odo['median_odo'] = myear_med_odo['model_year'].apply(get_median_odo)
myear_med_odo = myear_med_odo.set_index('model_year').median_odo
vehicles['odometer'] = vehicles['odometer'].fillna(vehicles['model_year'].map(myear_med_odo))

# Fill missing values in paint_color indiscriminately.
vehicles['paint_color'].fillna('unknown',inplace=True)

# Fill missing values in is_4wd. It probably isn't.
vehicles['is_4wd'].fillna(0,inplace=True)

# Convert float fields to more appropriate int type.
vehicles['model_year'] = vehicles['model_year'].astype(int)
vehicles['cylinders'] = vehicles['cylinders'].astype(int)
vehicles['odometer'] = vehicles['odometer'].astype(int)
vehicles['is_4wd'] = vehicles['is_4wd'].astype(int)

# Try to keep only one record per vehicle, based on latest advertisement.
vehicles.sort_values('date_posted',inplace=True)
vehicles.drop_duplicates(['model_year','model','odometer'], keep='last', inplace=True)

# Specify models of interest (pickup trucks only).
pickup_models = ['ford f-150', 'ford f-250', 'ford f-350', 'ford ranger', 'toyota tacoma', 'toyota tundra', \
                 'chevrolet colorado', 'chevrolet silverado', 'ram 1500', 'ram 2500', 'ram 3500', 'gmc sierra', \
                 'nissan frontier', 'dodge dakota']

# Filter dataframe to rows where 'model' contains a string from list of known pickup_models
# https://stackoverflow.com/questions/61158898/filter-pandas-where-some-columns-contain-any-of-the-words-in-a-list
pickups = vehicles[vehicles['model'].str.contains('|'.join(pickup_models))]

# add 'make' column to simplify comparisons by make
pickups['make'] = pickups['model'].apply(getmake)



###
### Data presentation
###

st.header('How does a pickup truck\'s make affect its value?')

st.write("Working with data from approximately a year of used car advertisements, I'll start by \
          comparing advertised prices for three makes of pickup truck that are well-represented in \
          our dataset.")

# Graph 1: Price histogram: Ford, Chevrolet, Ram
big3price = pickups.query("make in ['ford', 'chevrolet', 'ram']")[['price','make']]
big3price_hist = px.histogram(big3price, x="price", color="make", barmode="overlay",title="Price Frequencies by Make, Three Major Automakers")
big3price_hist.update_layout(yaxis_title_text = 'Number of Trucks Advertised',xaxis_title_text = 'Price')
st.plotly_chart(big3price_hist)
# This is the checkbox. It doesn't work, but please review the rest of my code while I figure this out
hist1check = st.checkbox("Show this graph without prices over $100,000", value=False)
if hist1check:
    del big3price_hist
    big3price = pickups.query("make in ['ford', 'chevrolet', 'ram'] & price < 100000")[['price','make']]
    big3price_hist = px.histogram(big3price, x="price", color="make", barmode="overlay",title="Price Frequencies by Make, Three Major Automakers")
    big3price_hist.update_layout(yaxis_title_text = 'Number of Trucks Advertised',xaxis_title_text = 'Price')
    st.plotly_chart(big3price_hist)

st.write("The median price for Chevrolet trucks appears to be a little higher than it is for Ford. \
          There are fewer Ram truck advertisements in our dataset, but the median sale price for \
          these is even higher. There are proportionately more lower-end trucks advertised for Ford \
          and Chevrolet than there are for Ram.")

st.write("Let's take the Ram price histogram and compare it with Dodge and Nissan. The \
          histograms for these makes will look substantially different from the other ones.")

# Graph 2: Price histogram: Ram, Dodge, Nissan
rdnprice = pickups.query("make in ['ram','dodge','nissan'] & price < 150000")[['price','make']]
rdnprice_hist = px.histogram(rdnprice, x="price", color="make", barmode="overlay",title="Price Frequencies by Make: Ram, Dodge, Nissan")
rdnprice_hist.update_layout(yaxis_title_text = 'Number of Trucks Advertised',xaxis_title_text = 'Price')
st.plotly_chart(rdnprice_hist)

st.write("(Prices above $150,000 have been excluded from this graph for clarity.)")
st.write("Dodge is firmly at the low end, but that's because the only model classified as Dodge in \
          our dataset is the Dodge Dakota, which is an older model. Ram is a offshoot of the Dodge \
          brand; if we treat Ram and Dodge as being the same maker, the older Dodge trucks would \
          fill out the lower end of the Ram histogram and make the distribution look a little more \
          like Chevrolet or Ford.")

st.write("Nissan, on the other hand, is interesting -- sale prices never seem to be above $25000, \
          half the asking price for some Ram trucks, but the distribution doesn't skew towards the \
          lower end. Could it be that Nissan trucks retain value, even if the base value is lower \
          overall? Let's look at a scatter plot.")

# this is the scatter plot
scatterfig = px.scatter(pickups.query('price < 100000 & model_year >= 1980'), x='model_year', y='price', color='make', hover_data=['model','condition','odometer'], title='Advertised Sale Price by Model Year, All Pickup Makes')
scatterfig.update_layout(yaxis_title_text='Price',xaxis_title_text='Model Year')
st.plotly_chart(scatterfig)

st.write("(Vehicles made before 1980, and those with sale prices above \$100000, have been excluded \
          from this chart to make it more readable.)")

st.write("We expect to see lower sale prices for older cars, but if Nissan trucks \"retained value\" \
          especially well, on a graph like this, the overall slope of the scatter cloud would be \
          less inclined than that of competing makes. That doesn't seem to be the case overall; \
          however, Nissan value does seem to hold its own compared to Dodge trucks for the same \
          model year. (Ram trucks are more expensive to begin with.) Actually, it looks like \
          Chevrolet has some of the highest sale prices for trucks made before 1995 -- they may be \
          the value retention champion.")

st.header("Conclusions")

st.write("The first charts we looked at explored the relationship between pickup truck make and \
          advertised sale price. There is some variation in distribution between makes; more Ford \
          trucks and fewer Dodge trucks appear at the low end of the price distribution. After \
          looking at data for some less popular makes, though, another question arose: what make of \
          trucks retain value? The scatter plot displays the relationship between truck model year \
          and advertised sale price, and by looking at different makes overlaid upon one another, I \
          found that Chevrolet in particular seems to sell for relatively higher prices among \
          pre-1995 trucks.")