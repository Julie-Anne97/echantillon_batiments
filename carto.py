import pandas as pd
import streamlit as st
import pydeck as pdk
import folium
from streamlit_folium import st_folium


#import & clean data

df = pd.read_parquet("C:\\Users\\jarosquin\\Documents\\opendatacarto\\.streamlit\\03-MASTERDATASET-job_part00000.parquet.snappy", engine='pyarrow')

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

# st.map(df3, zoom=None, use_container_width=True)

# st.write("Liste complète avec les filtres sélectionnées")
# st.dataframe(df3)

# def convert_df(df3):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df3.to_csv().encode('utf-8')

# csv = convert_df(df3)

# st.download_button(
#     label="Télécharge moi",
#     data=csv,
#     file_name='large_df.csv',
#     mime='text/csv')

# center on Liberty Bell, add marker
# m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
# folium.Marker(
#     [39.949610, -75.150282], 
#     popup="Liberty Bell", 
#     tooltip="Liberty Bell"
# ).add_to(m)

# tile = folium.TileLayer(
#         tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
#         attr = 'Esri',
#         name = 'Esri Satellite',
#         overlay = False,
#         control = True
#        ).add_to(m)

# call to render Folium map in Streamlit
# st_data = st_folium(m, width = 725)

df3['lat'] = df3['lat'].astype(float)
df3['lon'] = df3['lon'].astype(float)

df4 = df3[['lat', 'lon','libelleVoieEtablissement']].copy()

latitude = list(df3['lat'])
longitude = list(df3['lon'])
name = df3["libelleVoieEtablissement"]




map = folium.Map(location=[46.227638, 2.213749], zoom_start=7, control_scale=True)

tile2 = folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = False,
        control = True
       ).add_to(map)


# for index, location_info in df4.iterrows():
#     folium.Marker([df4["lat"], df4["lon"]], popup=location_info["libelleVoieEtablissement"]).add_to(map)
    
    
for index,lat in enumerate(latitude):
    folium.Marker([lat,longitude[index]],popup=name).add_to(map)
     

st_data = st_folium(map,width = 725)


# st.pydeck_chart(pdk.Deck(
#      map_style='mapbox://styles/mapbox/satellite-v9',
#      initial_view_state=pdk.ViewState(
#          latitude=46.227638,
#          longitude=2.213749,
#          zoom=9,
#          pitch=50,
#      ),
#      layers=[
#          pdk.Layer(
#             'HexagonLayer',
#             data=df3,
#             get_position='[lon, lat]',
#             radius=200,
#             elevation_scale=4,
#             elevation_range=[0, 1000],
#             pickable=True,
#             extruded=True,
#          ),
#          pdk.Layer(
#              'ScatterplotLayer',
#              data=df,
#              get_position='[lon, lat]',
#              get_color='[200, 30, 0, 160]',
#              get_radius=200,
#          ),
#      ],
#  ))
