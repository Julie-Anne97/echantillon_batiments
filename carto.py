import pandas as pd
import streamlit as st


#import & clean data

df = pd.read_parquet("03-MASTERDATASET-job_part00000.parquet.snappy", engine='pyarrow')

pd.set_option('display.max_columns',None)
df.head()
df = df.rename(columns={'latitude' : 'lat' , 'longitude' : 'lon'})
df = df.dropna(subset=['lat', 'lon'])
df.info(verbose=True, null_counts=True)

df = df.drop(df.iloc[:,72:94],axis=1)
df.reset_index()
df.info(verbose=True, null_counts=True)

df.adedpe202006_mean_class_estim_ges.unique()
classedpe = list(df.adedpe202006_mean_class_estim_ges.unique())

df = df.dropna(subset=['SURF_HAB_TOTAL'])

#Streamlit UI

st.title('Test Master dataset')

#Filtres

dpe = ["A", "B","C", "D", "E", "F", "G", "N"]
dpeselect = st.multiselect('Classe dpe :', classedpe,dpe)

surfaces = st.slider('Sélectionner la surface',0.0,10000.00,(0.00,10000.00),step=200.00)

df2 = df[df["adedpe202006_mean_class_estim_ges"].isin(dpeselect)]
df3 =  df2[df2["SURF_HAB_TOTAL"].isin(surfaces)]

#df3 = [df["SURF_HAB_TOTAL"].isin(surfaces)]
#df4 = df[df["adedpe202006_mean_class_estim_ges"].isin(dpeselect)][df["SURF_HAB_TOTAL"].isin(surfaces)]

st.map(df3, zoom=None, use_container_width=True)

st.write("Liste complète avec les filtres sélectionnées")
st.dataframe(df3)
