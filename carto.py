import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd 
from folium.plugins import MarkerCluster


#import data
df = pd.read_parquet("reducedfile.parquet.snappy", engine='pyarrow')

pd.set_option('display.max_columns',None)
df.head()

df = df.rename(columns={'latitude' : 'lat' , 'longitude' : 'lon'})
df = df.dropna(subset=['lat', 'lon'])
df.info(verbose=True, null_counts=True)

df = df[["lat","lon","siret", "siren", "id_ban","enseigne1Etablissement"]]
df.shape
df= df.drop_duplicates()
df.shape

df['entreprise'] = df[['siret', 'siren', 'id_ban',"enseigne1Etablissement"]].to_dict(orient='records')
df


#df = df[["SURF_HAB_TOTAL","lat","lon","geombui","adedpe202006_mean_class_estim_ges"]]
df.reset_index()


#Add filter

st.title('Test Master dataset')

#Filtres

dpe = ["A", "B","C", "D", "E", "F", "G", "N"]


surfaces = st.slider('Sélectionner la surface',0.0,10000.00,(0.00,10000.00),step=200.00)

# df2 = df[df["adedpe202006_mean_class_estim_ges"].isin(dpeselect)]
# df3 =  df2[df2["SURF_HAB_TOTAL"].isin(surfaces)]


bat_location = df[["lat","lon","entreprise"]]

# center on Aix 
m = folium.Map(location=[45.68422679091273, 5.909982061873071], zoom_start=7)



# add Google Tile
tile = folium.TileLayer(
        tiles = 'http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga',
        attr = 'Google',
        name = 'Google Hybrid',
        overlay = False,
        control = True
       ).add_to(m)


marker_cluster = folium.plugins.MarkerCluster().add_to(m)

for index, location_info in bat_location.iterrows():
    folium.Marker([location_info["lat"], location_info["lon"]], popup=[location_info["entreprise"]]).add_to(marker_cluster)

# call to render Folium map in Streamlit
st_map = st_folium(m, width = 725)

