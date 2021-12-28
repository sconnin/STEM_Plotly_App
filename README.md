# STEM_Plotly_App

This repo contains code/data used to create a web-application (https://stem-div.herokuapp.com/) for scoring/tracking diversity in STEM programs at the undergraduate level, nationwide. Specifically, the application provides a Simpson Index of Diversity score in relation to STEM completion data by institution and year. The results are further disaggregated by select institutional factors. 

The application is intended for use by: STEM educators, campus officers, industry recruiters, students 

The data were collected from the IPEDS portal (https://nces.ed.gov/ipeds/use-the-data) and subsequently cleaned/transformed for use with this application. Additional description is included in the application. 

The data hosted here include:

1. ethnic_perc_plotly.csv  -  percentage data for racial categories (STEM graduates) by institution and year 
2. stem_inst_diversity_coeff.csv - results of linear model applied to Simpson's Index of Diversity data by institution (2010-2020)
3. stem_inst_diversity_plotly.csv - diversity metrics by institution and year

Code for the web application:

1. stem_app.py

This project is ongoing - updates are planned to incorporate data on gender and disciplinary field. 
