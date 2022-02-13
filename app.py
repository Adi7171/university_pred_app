
import numpy as np
import pickle
import streamlit as st
import pandas as pd
import sklearn

loaded_model = pickle.load(open('trained_model.sav','rb'))

input_data = [[315,115,3,4.5,5,8.9,0]]

df=pd.read_csv('qs_Rankings.csv')

# def uni_rate(uni_name):
#     rating = df[df['university_name'] == uni_name ]['University Rating']
#     return rating
    # st.write(rating)
    # st.write("University Rating: ",rating)
# uni_name = input()
# rating = df[df['university_name'] == uni_name ]['University Rating']

def normalise(uni_name,prediction):
    sc = df[df['university_name'] == uni_name ]['score']
    nm = sc-prediction
    return round(float(nm),2)

def predict(input_data):
    inputdata = np.asarray(input_data).reshape(1,-1)
    pred = loaded_model.predict(inputdata)
    val = int(round(pred[0]*100,0))
    return val

def main():
    st.title("University Predictor App")
    uni_name = st.selectbox(
     'How would you like to be contacted?',
     (df[df['score']>0]['university_name']))
    # rating = uni_rate(uni_name)

    # st.write(rating)
    # GRE Score,TOEFL Score,University Rating,SOP,LOR ,CGPA,Research,
    
    gre_score = st.slider('GRE Score',260,340,315)
    toefl_score = st.slider('TOEFL Score',0,120,10)
    sop_score = st.slider('SOP Score',0.0,5.0,0.0,step=0.1)
    lor_score = st.slider('LOR Score',0.0,5.0,0.0,step=0.1)
    uni_rate = st.slider('UG College Score',0,5,0)
    cgpa = st.slider('CGPA',0.0,10.0,0.0,step=0.1)
    research = st.selectbox(
     'Research (Good quality then give 1)',
     (0,1))

    if st.button('University Chance predict'):
        input_data = [gre_score,toefl_score,uni_rate,sop_score,lor_score,cgpa,research]
        prediction = predict(input_data)
        if prediction <0:
            prediction=0
        if prediction >100:
            prediction=100

        ans = normalise(uni_name,prediction)
       
        st.markdown("### {prediction}% chance of getting admission into top 500 universties with this profile".format(prediction=prediction))
        if ans <=7.0:
            st.success("You have chance of getting an admit in {uni_name}".format(uni_name=uni_name))
        elif (ans>7.0 and ans<=12.0):
            st.warning("You Might or might not get admission in {uni_name}".format(uni_name=uni_name))
        elif (ans>12.0 and ans<=15.0):
            st.warning(f"Its your risk whether to apply or not to {uni_name}")
        else:
            st.error("You are in low chance of getting admission")

if __name__=='__main__':
    main()

