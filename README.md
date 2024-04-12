# sprint-4-project

The live Render instance of this project can be found here:
https://sprint-4-project-756x.onrender.com/

### Summary

This is a simple data visualization exercise, demonstrating use of Plotly Express graphs in a Streamlit web app.

It draws upon data from car sales advertisements over the course of a year to suggest possible conclusions about the relationship between maker, sale price, and sale speed, for pickup truck models in the dataset.

The Streamlit app is mainly for displaying graphs and doesn't get too deep into my process for analyzing the data. If you're interested in that, there's a writeup in the EDA.ipynb Jupyter notebook found in the /notebooks directory.

### Running the web app

This app is written in Python 3 and depends on several libraries to work. It has been tested to work with the following package versions, which are used for the Render instance:

pandas 2.0.3
scipy 1.11.1
streamlit 1.25.0
altair 5.0.1
plotly 5.15.0
numpy 1.25.2

You can run it on your own machine if you wish, if a Python environment is installed. Download and extract the project files, and open the project folder in the Terminal. To install the above dependencies, run:

`pip install streamlit && pip install -r requirements.txt`

Once the packages are installed, the app can be launched with `streamlit run app.py`.

The output of this command should direct you to http://0.0.0.0:10000 to view it in a browser.