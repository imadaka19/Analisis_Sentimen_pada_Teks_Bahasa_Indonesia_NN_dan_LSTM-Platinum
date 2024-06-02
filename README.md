# Analisis Sentimen pada Teks Bahasa Indonesia Menggunakan NN dan LSTM

This project is a challenge from Binar Academy aimed at building an API for cleansing also predicting sentiment from text, trained using data from [IndoNLU](https://github.com/IndoNLP/indonlu/tree/master/dataset/smsa_doc-sentiment-prosa) and conducting a comprehensive analysis.
## Before Instalation, Please download following files:
Place the downloaded files to model folder
- file LSTM [model/model.h5](https://drive.google.com/file/d/1SkQ9Wp4l7eekU2LF-VEE312WBb3LUzeQ/view?usp=sharing)
- file NN [model/model.p](https://drive.google.com/file/d/1qi1BomarBUhisrLOkt8dmG5-4oGJBsLH/view?usp=sharing)

## Installation

To get started, install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage

Run the application using the following command:

```bash
python app.py
```

## API

Access the API documentation by opening [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs) in your browser. The API offers two endpoints:

### 1. predict_text

This endpoint requires inputting text and choosing model from the dropdown button.

```http
  POST /predict_text
```

![image](https://github.com/imadaka19/F-DSC24001074-18-Kelompok-1-Analasis-Sentimen-dan-Klasifikasi-Platinum/assets/74599441/cbd00d04-fccf-4e92-9033-e6ca7f6e5479)


### 2. /text_predict_file

This endpoint requires inputting a CSV or TXT file with just 1 text column and you must choose the model from the dropdown button.

```http
  POST /text_predict_file
```

![image](https://github.com/imadaka19/F-DSC24001074-18-Kelompok-1-Analasis-Sentimen-dan-Klasifikasi-Platinum/assets/74599441/c0bd668c-8f00-4132-bc5b-520a9c0c02f9)


Those APIs will automatically import data to database as **data_table**.

The database will be saved in your local named **"challenge_database.db"**

Feel free to explore and integrate these APIs for effective cleansing and sentiment analysis of Indonesian Text.

## Contributors

Thanks to these amazing contributors:

- [@imadaka19](https://github.com/imadaka19) 
- [@ardhinihendiani](https://github.com/ardhinihendiani) 
- [@tasyaashil](https://github.com/tasyaashil)
