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

tab1, tab2, tab3 = st.tabs(["Home", "Dataset", "Analisis"])
with tab1:

    st.markdown("""
### Latar Belakang
**ABD** kepanjangan dari **Ayam Bang Dava** merupakan salah satu
franchise *fast food* lokal yang populer dengan 
olahan daging ayam kekinian. Populernya adalah hidangan
**"Ayam Geprek"**-nya. 

Ayam geprek di sini disajikan dengan beragam jenis sambal. 
Sambal original dan sambal daun jeruknya paling andalan. 
Seporsinya bisa disajikan dengan nasi putih, nasi merah, 
nasi cabe garam, nasi pedas merah, nasi pedas daun jeruk.
Menu yang banyak dipesan adalah **"Paket Komplit Nasi Ayam Geprek Sambal Matah"**.

***Unique Selling Point*** dari **ABD** ini adalah *fried kailan* yang ada di beberapa
menu makanannya dan juga tersedia sebagai *ala-carte*. *Fried kailan* sebagai pelengkap pada menu
beberapa hidangan ayam geprek mendampingi rasa *crispy* dari ayam geprek
bertemu dengan serat dan gurihnya dari *fried kailan* sehingga menciptakan
perpaduan rasa yang baru.

Seluruh ragam olahan menu tersebut dikemas 
menggunakan piring rotan untuk makan di tempat (*dine-in*), 
dan kotak food grade berwarna merah untuk *takeaway*. 
*Franchise* ini juga menggunakan beberapa aplikasi untuk melakukan pengantaran makanan
agar dapat menjangkau konsumennya. Salah satunya menggunakan layanan **GoFood** dari aplikasi **Gojek**.

Bisnis *fast food* terlihat cukup menguntungkan dibandingkan
dengan bisnis sektor lainnya. Dengan fokus *target market*-nya adalah mahasiswa dan pekerja kantoran.
Tentu dengan harga hidangan murah akan lebih disukai dan banyak diincar oleh konsumen.
Tidak hanya itu, mengusung penjualan makanan dengan konsep "Ayam Geprek" ini bisa dijadikan
sebagai makanan *"comfort-food"* akan sering dibeli karena terjangkau dan banyak hidangan pelengkap
untuk menemani makan.

Dalam kondisi diterpa pandemi tahun 2020, **ABD** menjadi semakin berkembang pesat dan 
hanya berfokus pada konsep *delivery online* atau bisa disebut dengan
*Virtual Restaurant*. Keberhasilan **ABD** di tahun 2020 dan 2021
melahirkan 27 *outlet* yang tersebar di Bandung, Jakarta, Cirebon, dan Tasikmalaya.
Adapun juga *outlet* lainnya yang baru hadir di sekitar Jabodetabek yang akan mendatang di tahun 2024.
""")

    st.divider()

    st.markdown("""
### Rumusan Masalah
Para kompetitor bisnis yang serupa dengan konsep jualan "Ayam Geprek" ini tentu belum
bisa mengungguli kompetitor besar lainnya. Maka dari itu, pentingnya sebuah *product knowledge* dan
*improvement* agar bisa bersaing secara kreatif dan mengusung teknik *marketing* dan *selling* yang bisa mendorong
berkembangnya suatu bisnis dengan harapan konsumen akan melakukan *repeat order*.

Untuk melakukan *improvement* terhadap bisnisnya, tentunya masukan dari konsumen juga sangat berarti
bagi pertumbuhan bisnisnya. Bisnis akan berkembang dan *sustainable* ketika segala *SOP* menjadi suatu acuan
dalam menjalankan suatu bisnis. Hal ini tentunya akan mendapatkan perlakuan yang berbeda yang membuat
faktor ini sulit menjadi pondasi dasar bersama untuk skala *middle manager* dan dibawahnya untuk
mengurusi setiap *outlet* dengan SDM yang beragam. Tentu saja, setiap *outlet* akan ada perbedaannya
dengan *outlet* yang lain dipengaruhi oleh SDM yang dimilikinya serta dari lingkungannya.

Hadirnya suatu *feedback* akan sangat berarti untuk mempertahankan bisnisnya serta mempererat hubungannya antara pelanggan
dan *outlet* terdekatnya agar mendapatkan suatu *improvement* dan perbaikan apabila ada kesalahan dalam memasarkan produknya.
Baik itu mendapatkan respon baik ataupun komentar, tentunya akan mengubah performa dari *franchise* tersebut agar bisa
diterima baik di lingkungan dan kepada masyarakat luas untuk mencoba dan menyantap dari produk ABD ini.
 
Oleh sebab itu, *project* ini berupaya untuk membangun sistem pendukung keputusan dalam menilai suatu produk dan
perbaikan *SOP*, *improvement*, maupun *product knowledge* dari setiap *outlet* agar dapat memiliki kualitas yang sama
sesuai dengan ekspektasi. Pada *project* ini juga dilakukan analisis untuk menguji beberapa hipotesis, di antaranya:
1. Apakah *review* berpengaruh pada penjualan?
2. Apakah sebagian besar *review* mengandung isi kata positif?
3. Seberapa besar pengaruh sebuah *review* terhadap penjualan?
""")
    st.divider()

    st.markdown("""
### Asumsi dan Batasan
Dalam pengerjaan *project* ini, terdapat beberapa asumsi dan batasan di antaranya:

1. Data sebuah *review* yang digunakan untuk analisis diambil dari *website* [GoFood](https://gofood.co.id).
2. Data yang didapatkan hanyalah yang muncul di kolom *review* berupa komentar atau pesan *feedback*.
""")

with tab2:

    st.header("Proses Pengambilan Data")
    
    st.markdown("""
Sebanyak 28 *outlet* ABD yang tersebar di kawasan Pulau Jawa, data yang berhasil ditarik sebanyak 4000 lebih menggunakan 
*software* Octoparse 8. Data tersebut diambil dan dilakukan *cleaning duplicate* dengan mengambil data *distinct* pada setiap
*outlet*-nya dalam bentuk *file excel (xlsx)*. Data yang didapatkan berupa **nama**, **inisial**, **waktu pembuatan akun**, **rating**,
**review**, **menu**, dan **tanggal pemesanan**. Karena ini melibatkan seluruh cabang, maka semua data yang ditarik akan menambahkan
satu kolom **lokasi** sebagai pembeda untuk masing-masing *outlet*.

""")
    st.image("https://raw.githubusercontent.com/w-arifin/testing-abd-ayam-bang-dava/main/image/sample_review.png", 
             caption="Salah satu contoh review dari ABD outlet Pasar Minggu", use_column_width=True, output_format='auto')

    st.markdown("""
Setelah mendapatkan data dari Octoparse 8 dan di *export* menjadi *file excel*,
data-data tersebut akan kembali diolah agar menjadi satu *dataset* yang akan menjadi patokan agar bisa untuk melakukan analisis dengan
membaginya ke beberapa dataset yang diperlukan untuk dianalisis satu per satu.
Setelah nantinya digabungkan, maka akan ada perubahan kolom yakni:

- Kolom "Title" berubah menjadi "**nama**"
- Kolom "Label" berubah menjadi "**inisial**"
- Kolom "Content" berubah menjadi "**user_since**"
- Kolom "ml1" berubah menjadi "**rating**"
- Kolom "breakword" berubah menjadi "**review**"
- Kolom "ml2" berubah menjadi "**menu**"
- Kolom "Content1" berubah menjadi "**order_date**"
- Kolom "Place" yang ditambahkan melalui *excel* berubah menjadi "**region**"

""")

    st.divider()
    st.header("Tampilan Dataset")
    st.markdown("""
    
Berikut adalah tampilan dataset yang telah melewati proses penggabungan data dari folder 
dataset serta dilakukan pemrosesan data. Data tersebut telah dilakukan transformasi pada kolom **inisial** sebagai *string*
dan pada kolom **user_since** dan **order_date** sebagai *datetime*. Berikut adalah contoh tabel dataset
dan *value* dibawah ini:

            """)
#Dataframe ini menggunakan random. Cek import dan kode ini.
    st.dataframe(data_clean.sample(n=10))

with tab3:
    #st.header("Total Menu")
    #st.dataframe(menu_counts)

    #st.header("Menu per Order date")
    #st.dataframe(menu_date_region)

    st.header("Penjualan Terbesar & Trend Penjualan ABD")
    st.subheader("Penjualan Menu Terlaris Franchise ABD")
    st.plotly_chart(fig)
    with st.expander("Legends:"):
         st.table(menu_counts.head(20))

    #with st.expander("Details:"):
        #st.markdown("""
#Terdapat sebanyak **7198** pesanan terjual dalam kurun waktu tahun 2019 hingga
#2024 dengan variasi menu sebanyak 518 menu yang terdaftar pada setiap *outlet*
#di berbagai daerah.

#Pada histogram diatas, terdapat penjualan terbesar yang pernah dijual
#oleh **ABD** yaitu **"Paket Komplit Nasi Ayam Geprek Sambal Matah"** dengan
#sebanyak 216 pesanan. Disusul dengan **"Ala Carte Ayam Geprek"** dengan jumlah
#188 pesanan.
                    #""")
    
    st.divider()
    st.subheader("Trend Penjualan Franchise ABD")
    
# ----------------------
# COLAB IN STREAMLIT 1: Making trend line chart
# ----------------------

    # Pilihan untuk tampilan grafik
    chart_view = st.radio("Chart View:", ("All Regions", "Selected Regions"), index=0)

    # Mengatur tata letak agar menjadi horizontal
    st.write("""
<style>
div.row-widget.stRadio > div {
    flex-direction: row;
}
div.row-widget.stRadio > div > label {
    margin-bottom: -20px;
}
</style>
""", unsafe_allow_html=True)

    if chart_view == "All Regions":
#--------
        # Pilihan Waktu
        col1, col2, col3 = st.columns(3)

        with col1:
            today = datetime.datetime.now()
            jan_1 = datetime.date(2019, 1, 1)

            d = st.date_input(
                "First Date to Last Date: ",
                (jan_1, today),
                jan_1,
                today,
                format="DD/MM/YYYY",
            )          

            output_d = tuple(date.strftime("%Y-%m-%d") for date in d)
            start_date, end_date = output_d

        # Filter data berdasarkan tanggal pemesanan antara 1 Januari 2020 hingga 31 Desember 2020
        menu_date_to_date = menu_date_region[(menu_date_region['order_date_item'] >= start_date) & (menu_date_region['order_date_item'] <= end_date)]

        # Kelompokkan berdasarkan bulan dan hitung total pesanan
        trend_data_all = menu_date_to_date.groupby(menu_date_to_date['order_date_item'].dt.to_period('M')).size().reset_index(name='total_orders')

        # Ubah nama kolom 'order_date_item' menjadi 'order_month' dan ubah tipe datanya menjadi string
        trend_data_all.rename(columns={'order_date_item': 'order_month'}, inplace=True)
        trend_data_all['order_month'] = trend_data_all['order_month'].astype(str)
    
        start_year = start_date[:4]
        end_year = end_date[:4]

        if start_year == end_year:
            output_year = start_year
        else:
            output_year = start_year + " - " + end_year

        # Judul grafik
        title_all = f"Trend Penjualan Bulanan ({output_year})"

        # Hitung rata-rata total pesanan
        average_orders = trend_data_all['total_orders'].mean()

        # Plot menggunakan Plotly
        fig_trend_all = px.line(trend_data_all, x='order_month', y='total_orders', title=title_all,
                        labels={'order_month': 'Bulan', 'total_orders': 'Total Pesanan'})

        # Tambahkan garis kurva rata-rata
        fig_trend_all.add_trace(go.Scatter(x=trend_data_all['order_month'], y=[average_orders] * len(trend_data_all),
                                        mode='lines',
                                        name='Rata-rata Pesanan',
                                        line=dict(color='red', dash='dash')))

        fig_trend_all.update_layout(barmode='group',
                        title={
                            'y': 0.9,  # Posisi judul secara vertikal (0-1)
                            'x': 0.5,  # Posisi judul secara horizontal (0-1)
                            'xanchor': 'center',  # Posisi judul berdasarkan pusat
                            'yanchor': 'top',  # Posisi judul berdasarkan atas
                            'font': {'size': 20}  # Ukuran font judul
                        },
                        width=700,  # Lebar gambar
                        height=400,  # Tinggi gambar
                        #paper_bgcolor='rgba(204, 255, 204, 0.5)',  # Warna latar belakang hijau mint transparan 50%
                        margin=dict(l=0, r=0, t=70, b=0)
                        )

        st.plotly_chart(fig_trend_all)

    else:

# Pilihan Waktu
        
        col1, col2, col3 = st.columns(3)

        with col1:
            today = datetime.datetime.now()
            jan_1 = datetime.date(2019, 1, 1)

            d = st.date_input(
                "First Date to Last Date:",
                (jan_1, today),
                jan_1,
                today,
                format="DD/MM/YYYY",
            )          

            output_d = tuple(date.strftime("%Y-%m-%d") for date in d)
            start_date, end_date = output_d

    # Pilihan Outlet
        unique_regions = menu_date_region['region'].sort_values().unique()

    # Menampilkan pilihan berdasarkan nilai unik dalam kolom "region"
        selected_options = st.multiselect('Select regions:', unique_regions, ['Sarijadi', 'Antapani', 'Buahbatu'])

    # Filter data berdasarkan tanggal pemesanan antara 1 Januari 2020 hingga 31 Desember 2020
        menu_date_to_date = menu_date_region[(menu_date_region['order_date_item'] >= start_date) & (menu_date_region['order_date_item'] <= end_date)]

    # Kelompokkan berdasarkan bulan dan wilayah, dan hitung total pesanan
        trend_data = menu_date_to_date.groupby([menu_date_to_date['order_date_item'].dt.to_period('M'), 'region']).size().reset_index(name='total_orders')

    # Daftar kota yang ingin Anda sertakan
        kota_trend = selected_options  # Anda bisa menambahkan nama-nama kota lainnya ke dalam list ini

    # Filter data untuk kota yang ingin disertakan
        trend_data_kota = trend_data[trend_data['region'].isin(kota_trend)].copy()

    # Ubah nama kolom 'order_date_item' menjadi 'order_month' dan ubah tipe datanya menjadi string
        trend_data_kota.rename(columns={'order_date_item': 'order_month'}, inplace=True)
        trend_data_kota['order_month'] = trend_data_kota['order_month'].astype(str)

        start_year = start_date[:4]
        end_year = end_date[:4]

        if start_year == end_year:
            output_year = start_year
        else:
            output_year = start_year + " - " + end_year

    # Judul grafik
        if len(selected_options) == 1:
            title = f"Trend Penjualan Bulanan di {selected_options[0]} ({output_year})"
        elif len(selected_options) == 2:
            title = f"Trend Penjualan Bulanan di {selected_options[0]} dan {selected_options[1]} ({output_year})"
        elif len(selected_options) == 3:
            title = "Trend Penjualan Bulanan di "
            for i in range(len(selected_options) - 1):
                title += f"{selected_options[i]}, "
            title += f"dan {selected_options[-1]} <br>({output_year})</br>"
        else:
            title = f"Trend Penjualan Bulanan ({output_year})"

    # Plot menggunakan Plotly
        fig_trend = px.line(trend_data_kota, x='order_month', y='total_orders', color='region', title=title,
                        labels={'order_month': 'Bulan', 'total_orders': 'Total Pesanan'})

        fig_trend.update_layout(barmode='group',
                        title={
                            'y': 0.9,  # Posisi judul secara vertikal (0-1)
                            'x': 0.5,  # Posisi judul secara horizontal (0-1)
                            'xanchor': 'center',  # Posisi judul berdasarkan pusat
                            'yanchor': 'top',  # Posisi judul berdasarkan atas
                            'font': {'size': 20}  # Ukuran font judul
                        },
                        width=700,  # Lebar gambar
                        height=400,  # Tinggi gambar
                        #paper_bgcolor='rgba(204, 255, 204, 0.5)',  # Warna latar belakang hijau mint transparan 50%
                        margin=dict(l=0, r=0, t=70, b=0)
                        )

        st.plotly_chart(fig_trend)
# ----------------------
# END OF COLAB IN STREAMLIT 1: Making trend line chart
# ----------------------
    
    with st.expander("Details:"):
        st.markdown("""
Terdapat sebanyak **7198** pesanan terjual dalam kurun waktu tahun 2019 hingga
2024 dengan variasi menu sebanyak 518 menu yang terdaftar pada setiap *outlet*
di berbagai daerah.

Pada histogram diatas, terdapat penjualan terbesar yang pernah dijual
oleh **ABD** yaitu **"Paket Komplit Nasi Ayam Geprek Sambal Matah"** dengan
sebanyak 216 pesanan. Disusul dengan **"Ala Carte Ayam Geprek"** dengan jumlah
188 pesanan.
                    """)
    
    st.divider()
    st.header('Review & Sentiment')
    st.subheader("Kata Terbanyak dalam Review")
    st.plotly_chart(fig_most_words)
    st.markdown("""
Kata-kata yang disematkan pada histogram ini merupakan kumpulan kata-kata yang banyak disematkan dan
seringkali diulang-ulang.

Pada histogram diatas, terdapat kata-kata yang terbesar adalah kata "enak" sebesar 1150.
Kata "enak" menunjukkan bahwa beberapa review menyematkan kata enak pada beberapa review.
Kata "enak" belum tentu memiliki makna baik pada setiap review yang ada seperti menyematkan
kata-kata negatif seperti kata "tidak", "enggak", "gak", dsb.
                """)
    
    st.divider()
    st.subheader("Bigram pada Review")

# ----------------------
# COLAB IN STREAMLIT 2: Making bigram chart
# ----------------------

    chart_view = st.radio("Chart View: ", ("All Regions", "Selected Regions"), index=0)

    # Mengatur tata letak agar menjadi horizontal
    st.write("""
<style>
div.row-widget.stRadio > div {
    flex-direction: row;
}
div.row-widget.stRadio > div > label {
    margin-bottom: -20px;
}
</style>
""", unsafe_allow_html=True)

    if chart_view == "All Regions":

        st.plotly_chart(fig_biplot)

        with st.expander("See explanation:"):
            st.markdown("""
                        **Bigram** merupakan pengolahan kalimat yang mengambil dua kata dalam satu kalimat yang sering muncul atau memiliki
                        frekuensi terbanyak. 
                            
                        - ***Node*** = Kata-kata yang sering muncul sebagai titik.
                            
                        - ***Line*** = Keterikatan antar kata yang membentuk suatu hubungan dengan garis
                            """)

        st.markdown("""
        Grafik bigram ini merupakan kumpulan kata-kata yang banyak disematkan dan
        seringkali diulang-ulang dan dijadikan garis hubung pada setiap kata ke kata dalam satu kalimat.

        Bigram diatas memiliki percabangan yang menunjukkan setiap kata dapat saling menyambung. 
        Namun, ada juga kata-kata yang membentuk percabangan sendiri seperti:
                    
        *Single-line*:
        - bang dava, ga sesuai.
                    
        *Multi-line*:
        - :red[**sambal**] matahnya, :red[**sambal**] matah, :red[**sambal**] daun jeruk.
        - :orange[**ayam**] geprek, :orange[**ayam**] popcorn, :orange[**nasi**] merah, :orange[**nasi**] merahnya, :orange[**nasi**] putih, :orange[**enak**] banget, :orange[**enak**] bgt, :orange[**enak**] rasanya.
        - nasi :green[**nya**] kurang banyak, sambel :green[**nya**] kurang banyak, ayam :green[**nya**] kurang banyak,
        ayam :green[**nya**] enak banget, ayam :green[**nya**] enak bgt, ayam :green[**nya**] enak rasanya,
        sambal :green[**nya**] enak banget, sambal :green[**nya**] enak bgt, sambal :green[**nya**] enak rasanya,
        nasi :green[**nya**] enak banget, nasi :green[**nya**] enak bgt, nasi :green[**nya**] enak rasanya.
                    """)
    else:
        regunique_regions = menu_date_region['region'].sort_values().unique()

    # Menampilkan pilihan berdasarkan nilai unik dalam kolom "region"
        regselected_options = st.multiselect('Select regions:', regunique_regions, ['Sarijadi', 'Antapani', 'Buahbatu'])

        region_data = reviews[reviews['region'].isin(regselected_options)].copy()

        tokenz_review = reviews['review'].astype(str)
        tokenz_review = tokenz_review.apply(emoticon_regex)

        region_tokenz_review = region_data['review'].astype(str)
        region_tokenz_review = region_tokenz_review.apply(emoticon_regex)
        # ----------------------
        # COLAB: Picking word
        # ----------------------
        regwords_in_review = [review.lower().split() for review in region_tokenz_review]
        regall_words = list(itertools.chain(*regwords_in_review))
        regcount_word_clean = collections.Counter(regall_words)

        # ----------------------
        # COLAB: Stopword Remover
        # ----------------------
        # Inisialisasi stopword untuk Bahasa Indonesia menggunakan Sastrawi
        stopword_factory = StopWordRemoverFactory()
        stop_words = stopword_factory.get_stop_words()

        # Menghapus stopword dari setiap review
        regreviews_non_stop = [[word for word in review if word not in stop_words] for review in regwords_in_review]

        # Menggabungkan semua kata yang tersisa menjadi satu daftar
        regall_words_nsw = list(itertools.chain(*regreviews_non_stop))

        # Menghitung frekuensi kata-kata yang tersisa
        regcounts_nsw = collections.Counter(regall_words_nsw)

        # ----------------------
        # COLAB: Stopword Remover
        # ----------------------
        regclean_reviews_nsw = pd.DataFrame(regcounts_nsw.most_common(15), columns=['words', 'count'])
        regfig_most_words = px.bar(regclean_reviews_nsw.sort_values(by='count'), 
                    x='count', 
                    y='words', 
                    orientation='h',
                    title='Common Words Found in Review (Without Stop Words)',
                    labels={'count':'Count', 'words':'Words'})

        regfig_most_words.update_layout(
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

        regbigram_words = [list(bigrams(review)) for review in regreviews_non_stop]
        # Mengambil data Bigram [QUESTION 7]
        regbigrams_list = list(itertools.chain(*regbigram_words))
        regbigram_counts = collections.Counter(regbigrams_list)
        regbigram_counts.most_common(30)

        # Membuat data Bigram DataFrame [QUESTION 8]
        regbigram_df = pd.DataFrame(regbigram_counts.most_common(20), columns=["bigram", "count"])
        ## Silahkan dapatkan variabel d untuk menjalankan grafik dibawah
        regd = regbigram_df.set_index("bigram").T.to_dict("records")

        # create network
        regG = nx.Graph()

        # create connection antar node
        for k, v in regd[0].items():
            regG.add_edge(k[0], k[1], weight =(v*2))

        # Get positions of nodes
        regpos = nx.spring_layout(regG, k=2)

        # Create edges
        edge_x = []
        edge_y = []
        for edge in regG.edges():
            x0, y0 = regpos[edge[0]]
            x1, y1 = regpos[edge[1]]
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
        for node in regG.nodes():
            x, y = regpos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)

        # Create figure
        regfig_biplot = go.Figure()

        # Add edges
        regfig_biplot.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(color='grey', width=5), hoverinfo='none'))

        # Add nodes
        regfig_biplot.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers', marker=dict(color='CadetBlue', size=10), text=node_text, hoverinfo='text'))

        # Add labels
        for key, value in regpos.items():
            x, y = value[0]+.075, value[1]+.075
            regfig_biplot.add_annotation(x=x, y=y, text=key, showarrow=False, font=dict(color='red', size=12), bgcolor='rgba(255,255,255,0.5)')

        # Judul grafik
        if len(regselected_options) == 1:
            regtitle = f"Bigram pada Kolom Review di {regselected_options[0]}"
        elif len(regselected_options) == 2:
            regtitle = f"Bigram pada Kolom Review di {regselected_options[0]} dan {regselected_options[1]}"
        elif len(regselected_options) == 3:
            regtitle = "Bigram pada Kolom Review di "
            for i in range(len(regselected_options) - 1):
                regtitle += f"{regselected_options[i]}, "
            regtitle += f"dan {regselected_options[-1]}"
        else:
            regtitle = f"Bigram pada Kolom Review"

        # Update layout
        regfig_biplot.update_layout(
            title={
                'text': regtitle,
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

        st.plotly_chart(regfig_biplot)

        with st.expander("See explanation:"):
            st.markdown("""
                        **Bigram** merupakan pengolahan kalimat yang mengambil dua kata dalam satu kalimat yang sering muncul atau memiliki
                        frekuensi terbanyak. 
                            
                        - ***Node*** = Kata-kata yang sering muncul sebagai titik.
                            
                        - ***Line*** = Keterikatan antar kata yang membentuk suatu hubungan dengan garis
                            """)

        st.markdown("""
        Grafik bigram ini merupakan kumpulan kata-kata yang banyak disematkan dan
        seringkali diulang-ulang dan dijadikan garis hubung pada setiap kata ke kata dalam satu kalimat.

        Bigram diatas memiliki percabangan yang menunjukkan setiap kata dapat saling menyambung. 
        Namun, ada juga kata-kata yang membentuk percabangan sendiri karena antar kata tersebut sifatnya mengikat dan
        tidak sebebas kata-kata lainnya dengan frekuensi hubungan yang tidak besar.
         
                    """)
    
# ----------------------
# END OF COLAB IN STREAMLIT 2: Making bigram chart
# ----------------------

    st.divider()
    st.subheader("Word Cloud pada Review")

# ----------------------
# COLAB IN STREAMLIT 3: Making Word Cloud
# ----------------------

    chart_view = st.radio("Chart View:", ("All Regions", "Selected Regions "), index=0)

    # Mengatur tata letak agar menjadi horizontal
    st.write("""
<style>
div.row-widget.stRadio > div {
    flex-direction: row;
}
div.row-widget.stRadio > div > label {
    margin-bottom: -20px;
}
</style>
""", unsafe_allow_html=True)

    if chart_view == "All Regions":

        text = one_word(" ".join(all_words_nsw))
        wordcloud = WordCloud(width=900, height=500, background_color="white").generate(text)

        fig = plt.figure(figsize=(15, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.tight_layout(pad=0)
        plt.axis("off")

        st.pyplot(fig)

        with st.expander("See explanation:"):
            st.markdown("""
                        ***Word cloud*** merupakan visualisasi dari banyaknya frekuensi kata-kata yang dituang pada satu wadah
                        besar yang memuat banyak kata dari yang terbanyak hingga terkecil. 
                            
                        Semakin besar ukuran pada suatu kata, maka kata tersebut memiliki frekuensi yang banyak.
                            
                        - **Font Besar** > Font Kecil
                        - **Frekuensi Banyak** > Frekuensi Kecil
                            """)

        st.markdown("""
        *Word cloud* kumpulan kata-kata yang disematkan dalam satu wadah yang memuat banyak kata yang sering muncul.
        Frekuensi pada kata sering kali muncul sebagai suatu kata yang mencolok lebih besar. *Word cloud* diatas menunjukkan terdapat kata-kata yang mencolok seperti kata "enak", "ayamnya", "nya", "ga", "yg", dsb.
        
        Dari [histogram sebelumnya](https://ominous-journey-69vrvrxr54j7c574q-8501.app.github.dev/?vscodeBrowserReqId=1710689961839#kata-terbanyak-dalam-review)
        terdapat kata dan frekuensi yang serupa seperti yang ada di *word cloud* diatas. Dalam bentuk visualisasi, setiap kata
        mendapatkan perbandingannya dengan kata lainnya yang dimuat dan memiliki makna yang jelas. Visualisasi dengan bentuk *word cloud* juga membantu dalam
        pembentukan *first impression* terhadap hasil analisisnya yang relevan dengan topik.
         
         
                    """)


    else:
        regunique_regions2 = menu_date_region['region'].sort_values().unique()

        # Menampilkan pilihan berdasarkan nilai unik dalam kolom "region"
        regselected_options2 = st.multiselect('Select regions: ', regunique_regions2, ['Sarijadi', 'Antapani', 'Buahbatu'])

        region_data2 = reviews[reviews['region'].isin(regselected_options2)].copy()

        tokenz_review2 = reviews['review'].astype(str)
        tokenz_review2 = tokenz_review2.apply(emoticon_regex)

        region_tokenz_review2 = region_data2['review'].astype(str)
        region_tokenz_review2 = region_tokenz_review2.apply(emoticon_regex)
            # ----------------------
            # COLAB: Picking word
            # ----------------------
        regwords_in_review2 = [review.lower().split() for review in region_tokenz_review2]
        regall_words2 = list(itertools.chain(*regwords_in_review2))
        regcount_word_clean2 = collections.Counter(regall_words2)

            # ----------------------
            # COLAB: Stopword Remover
            # ----------------------
            # Inisialisasi stopword untuk Bahasa Indonesia menggunakan Sastrawi
        stopword_factory = StopWordRemoverFactory()
        stop_words = stopword_factory.get_stop_words()

            # Menghapus stopword dari setiap review
        regreviews_non_stop2 = [[word for word in review if word not in stop_words] for review in regwords_in_review2]

            # Menggabungkan semua kata yang tersisa menjadi satu daftar
        regall_words_nsw2 = list(itertools.chain(*regreviews_non_stop2))

            # Menghitung frekuensi kata-kata yang tersisa
        regcounts_nsw2 = collections.Counter(regall_words_nsw2)

        regtext2 = one_word(" ".join(regall_words_nsw2))
        regwordcloud2 = WordCloud(width=900, height=500, background_color="white").generate(regtext2)

        regfig2 = plt.figure(figsize=(15, 10))
        plt.imshow(regwordcloud2, interpolation='bilinear')
        plt.tight_layout(pad=0)
        plt.axis("off")

        st.pyplot(regfig2)

        with st.expander("See explanation:"):
            st.markdown("""
                        ***Word cloud*** merupakan visualisasi dari banyaknya frekuensi kata-kata yang dituang pada satu wadah
                        besar yang memuat banyak kata dari yang terbanyak hingga terkecil. 
                            
                        Semakin besar ukuran pada suatu kata, maka kata tersebut memiliki frekuensi yang banyak.
                            
                        - **Font Besar** > Font Kecil
                        - **Frekuensi Banyak** > Frekuensi Kecil
                            """)

        st.markdown("""
        *Word cloud* kumpulan kata-kata yang disematkan dalam satu wadah yang memuat banyak kata yang sering muncul.
        Frekuensi pada kata sering kali muncul sebagai suatu kata yang mencolok lebih besar dari yang lainnya. Dari *word cloud*
        diatas di dominasi oleh kata "enak", "nya", dan "yg".
                    
        Pada setiap tempat yang dipilih pastinya terdapat perbedaan setiap *outlet*-nya mengakibatkan hasil dari *word cloud*-pun
        juga ikut berubah.
         
         
                    """)
        
# ----------------------
# END OF COLAB IN STREAMLIT 3: Making Word Cloud
# ----------------------

    st.divider()
    st.subheader('Sentimental Analysis dengan Text Blob pada Review')

# ----------------------
# COLAB IN STREAMLIT 4: Making Text Blob Sentiment Analysis
# ----------------------
    chart_view = st.radio("Chart View: ", ("All Regions", "Selected Regions "), index=0)

    # Mengatur tata letak agar menjadi horizontal
    st.write("""
<style>
div.row-widget.stRadio > div {
    flex-direction: row;
}
div.row-widget.stRadio > div > label {
    margin-bottom: -20px;
}
</style>
""", unsafe_allow_html=True)

    if chart_view == "All Regions":

        sentiment_objects = [TextBlob(review) for review in [" ".join(review) for review in reviews_non_stop]]
        sentiment_values = [[review.sentiment.polarity, str(review)] for review in sentiment_objects]
        sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "review"])

        sentiment_df_nozero = sentiment_df[sentiment_df["polarity"] != 0]

        figsent = figsent, ax = plt.subplots(figsize=(8, 6))
        # Membuat Histogram [QUESTION 12]
        sentiment_df_nozero.hist(column="polarity", bins=8, range=(-1,1), ax=ax)
        plt.title("Sentiments from Reviews", weight="bold")
        st.pyplot(figsent)
        
        with st.expander("See explanation:"):
            st.markdown("""
                        ***Sentimental Analysis*** atau analisis sentimen merupakan teknik analisis pada suatu kalimat untuk menilai
                        suatu kalimat apakah mengandung sebuah reaksi atau emosi baik itu positif atau negatif dalam pembandingan *polarity*. 
                            
                        *Polarity* merupakan pembandingan secara mutlak antara :green[nilai positif] dengan :red[nilai negatif]
                        pada suatu teks.
                            
                        - 0 < ***polarity*** < :green[**1**] = teks mengandung *polarity* positif
                        - 0 > ***polarity*** > :red[**-1**] = teks mengandung *polarity* negatif
                            """)
        
        rata_rata_sentiment = sentiment_df_nozero['polarity'].mean()
        rata_sentiment_adj = "{:.3f}".format(rata_rata_sentiment)
        modus_sentiment = sentiment_df_nozero['polarity'].mode()
        modus_polarity_string = ', '.join(map(str, modus_sentiment))

        st.markdown(f"""
        ***Sentimental Analysis*** umumnya menggunakan visualisasi histogram dengan menunjukkan bagaimana suatu kalimat atau teks dapat diolah
        dan dapat diketahui *polarity* yang menentukan apakah teks tersebut memiliki makna positif atau memiliki makna negatif.
        Melalui perbandingan antara nilai positif dan nilai negatif dalam histogram akan mudah mengetahui keseluruhan sebuah *review* berdasarkan
        teks di kolom *review*.
         
        Pada visualisasi histogram diatas, ditemukan frekuensi terbanyak pada rentang :green[**0.25**] hingga :green[**0.50**] lebih unggul di
        bagian *polarity* positif. Terdapat rata-rata *polarity* yaitu :green[**{rata_sentiment_adj}**] dan modus *polarity* yaitu :green[**{modus_polarity_string}**]. 
        
        Dalam rata-rata, *polarity* yang dibangun dari teks *review* memiliki makna positif berisikan *feedback* positif, saran positif, dan reaksi positif terhadap pesanannya oleh *customer*.
                    """)
    
    else:

        regunique_regions2 = menu_date_region['region'].sort_values().unique()

        # Menampilkan pilihan berdasarkan nilai unik dalam kolom "region"
        regselected_options2 = st.multiselect('Select regions: ', regunique_regions2, ['Sarijadi', 'Antapani', 'Buahbatu'])

        region_data2 = reviews[reviews['region'].isin(regselected_options2)].copy()

        tokenz_review2 = reviews['review'].astype(str)
        tokenz_review2 = tokenz_review2.apply(emoticon_regex)

        region_tokenz_review2 = region_data2['review'].astype(str)
        region_tokenz_review2 = region_tokenz_review2.apply(emoticon_regex)
            # ----------------------
            # COLAB: Picking word
            # ----------------------
        regwords_in_review2 = [review.lower().split() for review in region_tokenz_review2]
        regall_words2 = list(itertools.chain(*regwords_in_review2))
        regcount_word_clean2 = collections.Counter(regall_words2)

            # ----------------------
            # COLAB: Stopword Remover
            # ----------------------
            # Inisialisasi stopword untuk Bahasa Indonesia menggunakan Sastrawi
        stopword_factory = StopWordRemoverFactory()
        stop_words = stopword_factory.get_stop_words()

            # Menghapus stopword dari setiap review
        regreviews_non_stop2 = [[word for word in review if word not in stop_words] for review in regwords_in_review2]

            # Menggabungkan semua kata yang tersisa menjadi satu daftar
        regall_words_nsw2 = list(itertools.chain(*regreviews_non_stop2))

            # Menghitung frekuensi kata-kata yang tersisa
        regcounts_nsw2 = collections.Counter(regall_words_nsw2)


        regsentiment_objects = [TextBlob(review) for review in [" ".join(review) for review in regreviews_non_stop2]]
        regsentiment_values = [[review.sentiment.polarity, str(review)] for review in regsentiment_objects]
        regsentiment_df = pd.DataFrame(regsentiment_values, columns=["polarity", "review"])

        regsentiment_df_nozero = regsentiment_df[regsentiment_df["polarity"] != 0]

        regfigsent, ax = plt.subplots(figsize=(8, 6))
        # Membuat Histogram [QUESTION 12]
        regsentiment_df_nozero.hist(column="polarity", bins=8, range=(-1,1), ax=ax)
        plt.title("Sentiments from Reviews", weight="bold")
        st.pyplot(regfigsent)

        with st.expander("See explanation:"):
            st.markdown("""
                        ***Sentimental Analysis*** atau analisis sentimen merupakan teknik analisis pada suatu kalimat untuk menilai
                        suatu kalimat apakah mengandung sebuah reaksi atau emosi baik itu positif atau negatif dalam pembandingan *polarity*. 
                            
                        *Polarity* merupakan pembandingan secara mutlak antara :green[nilai positif] dengan :red[nilai negatif]
                        pada suatu teks.
                            
                        - 0 < ***polarity*** < :green[**1**] = teks mengandung *polarity* positif
                        - 0 > ***polarity*** > :red[**-1**] = teks mengandung *polarity* negatif
                            """)
        
        regrata_rata_sentiment = regsentiment_df_nozero['polarity'].mean()
        regrata_sentiment_adj = "{:.3f}".format(regrata_rata_sentiment)
        regmodus_sentiment = regsentiment_df_nozero['polarity'].mode()
        regmodus_polarity_string = ', '.join(map(str, regmodus_sentiment))

        st.markdown(f"""
        ***Sentimental Analysis*** umumnya menggunakan visualisasi histogram dengan menunjukkan bagaimana suatu kalimat atau teks dapat diolah
        dan dapat diketahui *polarity* yang menentukan apakah teks tersebut memiliki makna positif atau memiliki makna negatif.
        Melalui perbandingan antara nilai positif dan nilai negatif dalam histogram akan mudah mengetahui keseluruhan sebuah *review* berdasarkan
        teks di kolom *review*.

        Visualisasi pada *outlet-outlet* yang terpilih akan memiliki perbedaan setiap *outlet*-nya mengakibatkan hasil dari histogram tersebut
        juga ikut berubah. Dari *outlet* yang terpilih terdapat frekuensi terbanyak pada rentang :green[**0.25**] hingga :green[**0.50**] lebih unggul di
        bagian *polarity* positif dengan nilai *polarity*-nya yaitu :green[**{regmodus_polarity_string}**]. 
        
        Dengan rata-rata *polarity* yaitu :green[**{regrata_sentiment_adj}**] memungkinkan bahwa *polarity* yang dibangun dari teks *review* memiliki 
        makna positif berisikan *feedback* positif, saran positif, dan reaksi positif terhadap pesanannya oleh *customer*.
                    """)
# ----------------------
# END OF COLAB IN STREAMLIT 4: Making Text Blob Sentiment Analysis
# ----------------------

    st.divider()
    st.header("Kesimpulan")
    st.markdown("""
Berdasarkan dari sebuah data trend penjualan dan analisis sentimen, hasil analisis
tersebut menghasilkan beberapa poin yang dapat disimpulkan sebagai berikut:
                
1. Kolom *review* berpengaruh pada performa penjualan. Penjualan mempengaruhi performa
pada masing-masing *outlet* sebagai sarana pengembangan bisnis B2C yang mendapatkan respon berupa
*feedback* dari *product*-nya antara lain *compliment* berupa masukan positif maupun kritik dan saran untuk memperbaiki kualitas
dalam *product development* setiap *outlet*nya.

2. Sebagian besar *review* yang didapatkan dari keseluruhan cabang berupa *review* positif.
*review* positif disini ditunjukkan dari analisis sentimen yang sebagian besar polanya berada di condong positif.

3. Pengaruh *review* terhadap penjualan berada pada trend penjualan yang semakin hari bertambah terus seiring dengan
berjalannya waktu dan pembukaan *outlet-outlet* barunya. Hal ini menambahkan performa penjualan diatas rata-rata.
Dengan kolom review yang terbuka, *customer* dapat meyakinkan *customer* lainnya jika dalam suatu menu
diberikan *rating* dan *review* yang masuk akal dan meyakinkan.
                """)

    st.header("Saran")
    st.markdown("""
Pentingnya menjaga *customer relationship* dan *hospitality*-nya kepada *customer* baik saat
menerima pesanan dan pelayanannya. Beberapa menu andalan seharusnya bisa dijaga lebih baik lagi
dan menghindari adanya kelalaian yang berakibat reputasi *outlet* yang dipesannya bisa menurun. Selain itu, untuk menjaga
relasi kepada *customer* loyal, **ABD** harus siap untuk membuat menu *limited-edition* dan *marketing* 
agar bisa memancing *customer* untuk tidak berpikir panjang dalam pada pembelian dan memicu *repeat order*.                
                """)
