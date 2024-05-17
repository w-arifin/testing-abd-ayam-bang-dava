# import dari streamlit
import streamlit as st
from PIL import Image
# import dari google colab
import pandas as pd
import os
from datetime import datetime
import random
import matplotlib.pyplot as plt
import plotly.express as px
import datetime
import numpy as np
import plotly.graph_objects as go
import re
import itertools
import collections
import nltk
from nltk.corpus import stopwords
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import networkx as nx
from nltk import bigrams
from wordcloud import WordCloud
from textblob import TextBlob

# ----------------------
# COLAB: Start Section 1: Import Dataset
# ----------------------
data_concat = pd.read_excel('https://raw.githubusercontent.com/w-arifin/testing-abd-ayam-bang-dava/main/data/exported_data.xlsx')  
data_concat['inisial'] = data_concat['inisial'].astype(str)
# ----------------------
# COLAB: Convertion to datetime
# ----------------------
# Fungsi untuk mengonversi string menjadi objek datetime
def convert_to_date(string_date):
    parts = string_date.split(" ")
    date_str = " ".join(parts[-3:])  # Mengambil bagian tanggal, bulan, tahun
    return pd.to_datetime(date_str, format="%d %B %Y")

# Mengganti nilai di dalam kolom 'user_since' dan 'order_date' dengan format tanggal dd/mm/yy
data_concat['user_since'] = data_concat['user_since'].apply(convert_to_date)
data_concat['order_date'] = data_concat['order_date'].apply(convert_to_date)
# ----------------------
# COLAB: Cleaning null value
# ----------------------
data_clean = data_concat.dropna(subset=['menu'])
# ----------------------
# COLAB: End Section 1: Dataset Preparation
# ----------------------

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# ----------------------
# COLAB: Start Section 2: Making New Dataset jumlah_menu
# ----------------------
# Membuat DataFrame jumlah_menu
jumlah_menu = pd.DataFrame(data_clean)

# List untuk menyimpan menu-menu yang sudah dipisahkan
menus = []

# Variabel untuk menangani pengecualian
exception_phrases = ["Bantu Driver Ojol Dengan Cara Menraktir Mereka", "Traktir Driver  "]

# Iterasi melalui setiap frasa untuk menangani pengecualian
for value in jumlah_menu['menu']:
    # Mengubah prefix
    value = value.replace("Untuk Driver -", "Untuk Driver")
    value = value.replace("Traktir Driver -", "Traktir Driver")

    # Menghapus double space
    value = value.replace("  ", " ")

    # Menghapus tanda titik
    value_without_dot = value.replace(".", "")

    phrases = value_without_dot.split(" - ")
    i = 0
    while i < len(phrases):
        phrase = phrases[i]
        if any(phrase.startswith(exception) for exception in exception_phrases):
            combined_phrase = phrase
            while i + 1 < len(phrases) and any(phrases[i + 1].startswith(exception) for exception in exception_phrases):
                combined_phrase += " - " + phrases[i + 1]
                i += 1
            menus.append(combined_phrase)
        else:
            menus.append(phrase)
        i += 1

# Membuat DataFrame baru berdasarkan hasil
menu_counts = pd.DataFrame(menus, columns=['menu'])

# Menggabungkan nilai-nilai dengan memperhatikan kapitalisasi
menu_counts['menu'] = menu_counts['menu'].str.lower()  # Mengubah semua huruf menjadi huruf kecil

# Menghitung jumlah masing-masing menu
menu_counts = menu_counts.value_counts().reset_index(name='count')

# Mengubah nama header kolom
menu_counts = menu_counts.rename(columns={'menu': 'Menu', 'count': 'Jumlah'})

# ----------------------
# COLAB: Making New Dataset for menu_date_region
# ----------------------
# Membuat DataFrame
tanggal_menu = pd.DataFrame(data_clean)

# List untuk menyimpan menu-menu yang sudah dipisahkan
menus = []

# Variabel untuk menangani pengecualian
exception_phrases = ["Bantu Driver Ojol Dengan Cara Menraktir Mereka", "Traktir Driver  "]

# Iterasi melalui setiap frasa untuk menangani pengecualian
for value, order_date, region in zip(tanggal_menu['menu'], tanggal_menu['order_date'], tanggal_menu['region']):
    # Mengubah prefix
    value = value.replace("Untuk Driver -", "Untuk Driver")
    value = value.replace("Traktir Driver -", "Traktir Driver")

    # Menghapus double space
    value = value.replace("  ", " ")

    # Menghapus tanda titik
    value_without_dot = value.replace(".", "")

    phrases = value_without_dot.split(" - ")
    i = 0
    while i < len(phrases):
        phrase = phrases[i]
        if any(phrase.startswith(exception) for exception in exception_phrases):
            combined_phrase = phrase
            while i + 1 < len(phrases) and any(phrases[i + 1].startswith(exception) for exception in exception_phrases):
                combined_phrase += " - " + phrases[i + 1]
                i += 1
            menus.append((combined_phrase, order_date, region))
        else:
            menus.append((phrase, order_date, region))
        i += 1

# Membuat DataFrame baru berdasarkan hasil
menu_date_region = pd.DataFrame(menus, columns=['menu', 'order_date_item', 'region'])

# Menggabungkan nilai-nilai dengan memperhatikan kapitalisasi
menu_date_region['menu'] = menu_date_region['menu'].str.lower()  # Mengubah semua huruf menjadi huruf kecil

menu_date_region = menu_date_region.sort_values(by='order_date_item', ascending=False)

# ----------------------
# COLAB: End Section 2: Dataset Preparation
# ----------------------

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# ----------------------
# COLAB: Start Section 3: Making histogram menu
# ----------------------
fig = px.bar(menu_counts.head(20), x='Menu', y='Jumlah', title='Sales Performance in 2020', labels={'Sales': 'Total Profit'})

# Update layout for better visualization
fig.update_layout(barmode='group',
                  xaxis_title='State',  # Menambahkan bold pada judul sumbu x
                  yaxis_title='Count',
                  xaxis_visible=False,  # Menyembunyikan label sumbu x
                  title={
                      'text': '<b>Top 20 Highest Selling Menus</b>',
                      'y': 0.9,  # Posisi judul secara vertikal (0-1)
                      'x': 0.5,  # Posisi judul secara horizontal (0-1)
                      'xanchor': 'center',  # Posisi judul berdasarkan pusat
                      'yanchor': 'top',  # Posisi judul berdasarkan atas
                      'font': {'size': 20}  # Ukuran font judul
                  },
                  width=700,  # Lebar gambar
                  height=300,  # Tinggi gambar
                  #paper_bgcolor='rgba(204, 255, 204, 0.5)',  # Warna latar belakang hijau mint transparan 50%
                  margin=dict(l=0, r=0, t=55, b=0)
                  )

# ----------------------
# COLAB: End Section 3: Making histogram menu
    # For details, check COLAB IN STREAMLIT 1
# ----------------------

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# ----------------------
# COLAB: Start Section 4: Common Words
# ----------------------

# Membuat DataFrame
reviews = pd.DataFrame(data_clean)

# Membuat list untuk menyimpan menu-menu yang sudah dipisahkan
menu_lists = []

# Iterasi melalui setiap baris dataframe
for value in reviews['menu']:
    # Mengubah prefix
    value = value.replace("Untuk Driver -", "Untuk Driver")
    value = value.replace("Traktir Driver -", "Traktir Driver")

    # Menghapus double space
    value = value.replace("  ", " ")

    # Menghapus tanda titik
    value_without_dot = value.replace(".", "")

    # Membuat list dari menu-menu yang dipisahkan
    phrases = value_without_dot.split(" - ")

    # Menambahkan list menu-menu untuk baris tertentu ke dalam list utama
    menu_lists.append(phrases)

# Menambahkan list menu-menu ke dalam dataframe sebagai kolom baru
reviews['menu_lists'] = menu_lists

# ----------------------
# COLAB: Regex Deletion for Emoticon
# ----------------------
# Buat Function Regex untuk hapus emoticon
def emoticon_regex(text):
    # menghapus emoticon
    emoticon_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]'
    # mengambil hanya kata-kata
    text = re.sub(emoticon_pattern, '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

tokenz_review = reviews['review'].astype(str)
tokenz_review = tokenz_review.apply(emoticon_regex)

# ----------------------
# COLAB: Picking word
# ----------------------
words_in_review = [review.lower().split() for review in tokenz_review]
all_words = list(itertools.chain(*words_in_review))
count_word_clean = collections.Counter(all_words)

# ----------------------
# COLAB: Stopword Remover
# ----------------------
# Inisialisasi stopword untuk Bahasa Indonesia menggunakan Sastrawi
stopword_factory = StopWordRemoverFactory()
stop_words = stopword_factory.get_stop_words()

# Menghapus stopword dari setiap review
reviews_non_stop = [[word for word in review if word not in stop_words] for review in words_in_review]

# Menggabungkan semua kata yang tersisa menjadi satu daftar
all_words_nsw = list(itertools.chain(*reviews_non_stop))

# Menghitung frekuensi kata-kata yang tersisa
counts_nsw = collections.Counter(all_words_nsw)

# ----------------------
# COLAB: Stopword Remover
# ----------------------
clean_reviews_nsw = pd.DataFrame(counts_nsw.most_common(15), columns=['words', 'count'])
fig_most_words = px.bar(clean_reviews_nsw.sort_values(by='count'), 
             x='count', 
             y='words', 
             orientation='h',
             title='Common Words Found in Review (Without Stop Words)',
             labels={'count':'Count', 'words':'Words'})

fig_most_words.update_layout(
    title_xanchor='center',  # Posisi judul berdasarkan pusat secara horizontal
    title_yanchor='top',  # Posisi judul berdasarkan atas secara vertikal
    title='Common Words Found in Review (Without Stop Words)',
    xaxis_title='Count',
    yaxis_title='Words',
    title_x=0.5,  # Posisi judul secara horizontal (0-1)
    title_y=0.95,  # Posisi judul secara vertikal (0-1)
    title_font_size=20,  # Ukuran font judul
    width=700,  # Lebar gambar
    height=400,  # Tinggi gambar
    margin=dict(l=0, r=0, t=50, b=0),
    bargap=0.1  # Jarak antara batang dalam grup
)

# ----------------------
# COLAB: End Section 4: Common Words
# ----------------------

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# ----------------------
# COLAB: Start Section 5: Making Biplot Chart
# ----------------------

bigram_words = [list(bigrams(review)) for review in reviews_non_stop]
# Mengambil data Bigram [QUESTION 7]
bigrams_list = list(itertools.chain(*bigram_words))
bigram_counts = collections.Counter(bigrams_list)
bigram_counts.most_common(30)

# Membuat data Bigram DataFrame [QUESTION 8]
bigram_df = pd.DataFrame(bigram_counts.most_common(20), columns=["bigram", "count"])
## Silahkan dapatkan variabel d untuk menjalankan grafik dibawah
d = bigram_df.set_index("bigram").T.to_dict("records")

# create network
G = nx.Graph()

# create connection antar node
for k, v in d[0].items():
    G.add_edge(k[0], k[1], weight =(v*2))

# Get positions of nodes
pos = nx.spring_layout(G, k=2)

# Create edges
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

# Create nodes
node_x = []
node_y = []
node_text = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(node)

# Create figure
fig_biplot = go.Figure()

# Add edges
fig_biplot.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(color='grey', width=5), hoverinfo='none'))

# Add nodes
fig_biplot.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers', marker=dict(color='CadetBlue', size=10), text=node_text, hoverinfo='text'))

# Add labels
for key, value in pos.items():
    x, y = value[0]+.075, value[1]+.075
    fig_biplot.add_annotation(x=x, y=y, text=key, showarrow=False, font=dict(color='red', size=12), bgcolor='rgba(255,255,255,0.5)')

# Update layout
# Update layout
fig_biplot.update_layout(
    title={
        'text': 'Bigram pada Kolom Review',
        'x': 0.5,  # Posisi judul secara horizontal (0-1)
        'y': 0.95,  # Posisi judul secara vertikal (0-1)
        'xanchor': 'center',  # Posisi judul berdasarkan pusat
        'yanchor': 'top',  # Posisi judul berdasarkan atas
        'font': {'size': 20}  # Ukuran font judul
    },
    showlegend=False,
    plot_bgcolor='white',
    xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False, 'range': [-1.1, 1.1]},  # Adjust x-axis range
    yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False, 'range': [-1.1, 1.1]},  # Adjust y-axis range
    width=700,  # Lebar gambar
    height=500,  # Tinggi gambar
    margin={'l': 0, 'r': 0, 't': 70, 'b': 0}
)

# ----------------------
# COLAB: End Section 5: Making Bigram Chart
    # For details, check COLAB IN STREAMLIT 2
# ----------------------

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# ----------------------
# COLAB: Start Section 6: Making Word Cloud
# ----------------------

# Buat Function Regex untuk hapus satu huruf misal (S saja, atau M aja) [QUESTION 9]
def one_word(text):
    # pattern untuk menghapus satu huruf
    pattern = r'\b[a-zA-Z]\b'
    # mengganti satu huruf dengan string kosong
    text = re.sub(pattern, '', text)
    return text

# ----------------------
# COLAB: End Section 6: Making Word Cloud
    # For details, check COLAB IN STREAMLIT 3
# ----------------------

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# ----------------------
# COLAB: Start Section 7: Text Blob Sentiment Analysis
# ----------------------



# ----------------------
# COLAB: End Section 7: Text Blob Sentiment Analysis
    # For details, check COLAB IN STREAMLIT 4
# ----------------------




# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&


# ----------------------
# STREAMLIT : DESIGN SECTION!!
# ----------------------

st.set_page_config(
    page_title="Analisis Kepuasan Konsumen Franchise ABD (Ayam Bang Dava)",
    page_icon="https://raw.githubusercontent.com/w-arifin/testing-abd-ayam-bang-dava/main/image/image_2024-03-08_155100554-modified.png",
    layout="centered"
)

st.title("Analisis Kepuasan Konsumen Franchise ABD (Ayam Bang Dava)")
st.write("Wondy Arifin || Member of TETRIS Batch IV from DQLAB")

