from flask import Flask, jsonify
import re
import pandas as pd
import db
import clean
import pickle
import numpy as np
import tensorflow as tf

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

#### flask
app = Flask(__name__)\

###swager
app.json_encoder = LazyJSONEncoder
swagger_template = {
    "info": {
        "title":  "API Documentation for Data Preprocessing",
        "version": "1.0.0",
        "description": "Dokumentasi API"
    },
    "host": "127.0.0.1:5000"
}
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,
                  config=swagger_config)

## Import feature extraction BoW
file = open("Extraction File/NN/fe_nn.p", "rb")
count_vect = pickle.load(file)
file.close()

## Import NN model
file = open("model/model.p", "rb")
model_NN = pickle.load(file)
file.close()

## Import LSTM model
model_LSTM = tf.keras.models.load_model('model/model.h5')

## Import feature extraction pad sequences
file = open("Extraction File/LSTM/X_train_padded.pickle",'rb')
X = pickle.load(file)
file.close()

## Import feature extraction tokenizer
file = open("Extraction File/LSTM/tokenizer.pickle",'rb')
tokenizer_lstm = pickle.load(file)
file.close()

@swag_from("docs/predict_text.yml", methods=['POST'])
@app.route('/predict_text', methods=['POST'])
def input_teks():
    data = request.form.get('text')
    modelnya = request.args.get('model')

    dict = {
        'text':'', 
        'label':'', 
        'text_clean':''
    }
    dict['text'] = data
    
    data_cleaned = clean.clean_data(data) #clean data input
    dict['text_clean'] = data_cleaned

    if modelnya == "NN":
        # Feature Extraction
        text = count_vect.transform([data_cleaned])

        # Kita prediksi sentimennya
        result = model_NN.predict(text)[0]
        dict['label'] = result

    else :
        sentiment = ['negative', 'neutral', 'positive']

        # max_features = 100000
        # tokenizer = Tokenizer(num_words=max_features, split=' ', lower=True)
        predicted = tokenizer_lstm.texts_to_sequences([data_cleaned])
        guess = pad_sequences(predicted, maxlen=X.shape[1])

        prediction = model_LSTM.predict(guess)
        polarity = np.argmax(prediction[0])
        
        result = sentiment[polarity]
        # print("Text: ",text[0])
        # print("Sentiment: ",sentiment[polarity])
        dict['label'] = result
    
    db.create_text_db(dict)

    json_response = {
        'status_code': 200,
        'description': "Hasil predict",
        'Teks' : data,
        'Prediksi': result,
    }
    
    return jsonify(json_response)

@swag_from("docs/text_predict_file.yml", methods=['POST'])
@app.route('/text_predict_file', methods=['POST'])
def text_predict_file():

    # Upladed file
    file = request.files.getlist('file')[0]
    modelnya = request.args.get('model')

    lines = file.read().decode('utf-8').splitlines()  # Membaca file sebagai teks dan memisahkan baris
    df_file = pd.DataFrame(lines, columns=['text'])

    df_clean_rt_n = df_file.copy()
    
    df_file['text_clean'] = df_clean_rt_n['text'].apply(clean.clean_data)

    if modelnya == "NN":
        # Feature Extraction
        text = count_vect.transform(df_file['text_clean'])

        # Kita prediksi sentimennya
        result = model_NN.predict(text)
        df_file['label'] = result

    else :
        sentiment = ['negative', 'neutral', 'positive']

        text_sequences = tokenizer_lstm.texts_to_sequences(df_file['text_clean'])
        text_padded = pad_sequences(text_sequences, maxlen=X.shape[1]) 

        # Prediksi sentimen
        prediction = model_LSTM.predict(text_padded)
        if prediction.ndim == 1:
            polarity = np.argmax(prediction)
        else:
            polarity = np.argmax(prediction, axis=1)
        
        df_file['label'] = [sentiment[p] for p in polarity]

    db.create_db(df_file[['text','label','text_clean']])

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'hasil' : df_file[['text','label']].values.tolist(),
        # 'prediksi': df_file['label'].values.tolist(),
    }

    response_data = jsonify(json_response)

    return response_data


##running api
if __name__ == '__main__':
    app.run()