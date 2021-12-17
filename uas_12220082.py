
#Nama : Iftitah Nurul Putri Aqilah
#NIM: 12220082                    


import pandas as pd
import json
import matplotlib as plt
from matplotlib import cm
import streamlit as st


filepath = "produksi_minyak_mentah.csv"
df = pd.read_csv(filepath)
datajson = pd.read_json("kode_negara_lengkap.json")

df = df.set_index("kode_negara")
df = df.drop(["WLD","G20","OECD","OEU","EU28"])
df.reset_index(drop=False, inplace=True)

listkode = []
listorganisasi = []

for i in list(df['kode_negara']):
    if i not in listkode:
        listkode.append(i)

for i in listkode:
    if i not in list(datajson['alpha-3']):
        listorganisasi.append(i)

for i in listorganisasi:
    df = df[df.kode_negara != i]
    if i in listkode:
        listkode.remove(i)

listnama2 = []
listregion2 = []
listsubregion2 = []

for i in range(len(listkode)):
    for j in range(len(list(datajson['alpha-3']))):
        if list(datajson['alpha-3'])[j] == listkode[i] and list(datajson['name'])[j] not in listnama2:
            listnama2.append(list(datajson['name'])[j])
            listregion2.append(list(datajson['region'])[j])
            listsubregion2.append(list(datajson['sub-region'])[j])

df_sinkron = pd.DataFrame(list(zip(listnama2, listkode, listregion2, listsubregion2)), columns=['nama_negara', 'kode_negara', 'region', 'sub_region'])

#title
st.set_page_config(layout="wide")
st.title("Crude Oil Production of Each Country in the World")

#sidebar
st.sidebar.title("Sidebar")
Nama = st.sidebar.selectbox("Pilih Negara", listnama2)
left_col, right_col = st.columns(2)

#Soal 1A
st.subheader("Prduksi Negara")

for i in range(len(listnama2)):
    if listnama2[i] == Nama:
        kodenegarahuruf = listkode[i]
        region = listregion2[i]
        subregion = listsubregion2[i]

tahunsoal1 = []
produksisoal1 = []

for i in range(len(list(df['kode_negara']))):
    if kodenegarahuruf == list(df['kode_negara'])[i]:
        tahunsoal1.append(list(df['tahun'])[i])
        produksisoal1.append(list(df['produksi'])[i])

fig, ax = plt.subplots()
plt.plot(tahunsoal1, produksisoal1)
plt.title(Nama)
plt.xlabel('Tahun', fontsize = 12)
plt.ylabel('Produksi', fontsize = 12)
plt.show()
left_col.pyplot(fig)

#Soal 1B
st.subheader("Produksi Terbesar Pada Tahun Tertentu")
Tahun = st.sidebar.number_input("Pilih Tahun", min_value = 1971, max_value = 2015, value = 1990)
Berapa = st.sidebar.number_input("Banyaknya Negara", min_value = 1, max_value = None, value = 10)

dftahun = df.loc[df['tahun'] == Tahun].sort_values(by=['produksi'], ascending=False)

dftahunbanyak = dftahun[:Berapa]

negarasoal2 = dftahunbanyak['kode_negara']
produksisoal2 = dftahunbanyak['produksi']

fig, ax = plt.subplots()
plt.bar(negarasoal2,produksisoal2)
plt.show()
right_col.pyplot(fig)
