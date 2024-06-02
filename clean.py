import re
import pandas as pd
import db

#### cleansing data

stopword_table = db.read_db()

def remove_stopwords(data):
    return " ".join(x for x in data.split() if x not in stopword_table.stopword.values.tolist())

def clean_data(data):
    data = data.lower() #membuat semua huruf menjadi lower case
    data = data.strip() #menghapus white space di awal dan akhir
    data = re.sub('[^a-zA-Z0-9]+', ' ', data) #hapus selain alfanumeric
    data = remove_stopwords(data) #menghapus stopword
    data = data.strip() #menghapus white space di awal dan akhir
    return data