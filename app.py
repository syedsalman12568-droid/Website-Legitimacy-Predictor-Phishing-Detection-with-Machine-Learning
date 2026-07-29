import streamlit as st
import pandas as pd
import pickle

# Loading the trained model
model = pickle.load(open("phishing_model.pkl", "rb"))

st.title("Website Legitimacy Prediction")
st.write("This app predicts whether a website is Phishing or Legitimate based on some URL and website features.")

st.header("Enter Website Features")

# Note: in this dataset, 1 = suspicious/phishing-like feature, 0 = normal
# and the final Label is 1 = Phishing, 0 = Legitimate

Have_IP = st.selectbox("Does the URL have an IP address instead of a domain name?", [0, 1])
Have_At = st.selectbox("Does the URL contain an @ symbol?", [0, 1])
URL_Length = st.selectbox("Is the URL unusually long?", [0, 1])
URL_Depth = st.slider("URL Depth (number of '/' in the URL)", 0, 20, 3)
Redirection = st.selectbox("Does the URL have '//' redirection?", [0, 1])
https_Domain = st.selectbox("Does 'https' appear in the domain part itself?", [0, 1])
TinyURL = st.selectbox("Is it a shortened URL (like bit.ly)?", [0, 1])
Prefix_Suffix = st.selectbox("Does the domain have a '-' (prefix/suffix)?", [0, 1])
DNS_Record = st.selectbox("Is DNS record missing for this domain?", [0, 1])
Web_Traffic = st.selectbox("Does the website have low/no web traffic?", [0, 1])
Domain_Age = st.selectbox("Is the domain age less than 6 months?", [0, 1])
Domain_End = st.selectbox("Does the domain expire soon (within 6 months)?", [0, 1])
iFrame = st.selectbox("Does the page use iFrame?", [0, 1])
Mouse_Over = st.selectbox("Does the page use onMouseOver effects?", [0, 1])
Right_Click = st.selectbox("Is right click disabled on the page?", [0, 1])
Web_Forwards = st.selectbox("Does the page have too many redirects?", [0, 1])

# Putting all inputs into a dataframe for prediction
input_data = pd.DataFrame([[Have_IP, Have_At, URL_Length, URL_Depth, Redirection,
                             https_Domain, TinyURL, Prefix_Suffix, DNS_Record,
                             Web_Traffic, Domain_Age, Domain_End, iFrame,
                             Mouse_Over, Right_Click, Web_Forwards]],
                           columns=['Have_IP', 'Have_At', 'URL_Length', 'URL_Depth',
                                    'Redirection', 'https_Domain', 'TinyURL',
                                    'Prefix/Suffix', 'DNS_Record', 'Web_Traffic',
                                    'Domain_Age', 'Domain_End', 'iFrame',
                                    'Mouse_Over', 'Right_Click', 'Web_Forwards'])

if st.button("Predict"):
    prediction = model.predict(input_data)[0]
    prediction_proba = model.predict_proba(input_data)[0]

    if prediction == 0:
        st.error("This website is predicted as: LEGITIMATE ✅")
    else:
        st.success("This website is predicted as: PHISHING ⚠️")

    st.write("Prediction Probability:")
    st.write(f"Legitimate: {prediction_proba[0]*100:.2f}%")
    st.write(f"Phishing: {prediction_proba[1]*100:.2f}%")

st.write("---")
st.write("Made by Syed Salman Razvi | Mini Project - Website Legitimacy Prediction")
