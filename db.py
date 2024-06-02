import sqlite3
import pandas as pd

def read_db():
    conn = sqlite3.connect('dataset\challenge_database.db')
    #read stopword_table
    stopword_table = pd.read_sql_query("""
                    SELECT 
                        *
                    FROM stopword_table
                  """, conn)
    conn.close()
    return stopword_table
  

def create_db(df):
    conn = sqlite3.connect('dataset\challenge_database.db')
    cursor = conn.cursor()
    # data = list(zip(tweet, tweet_cleaned))
    #create tweet_table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS data_table (
        text TEXT,
        label TEXT,
        text_clean TEXT
    )
    ''')
    # tweet.to_sql('tweet_table', conn, if_exists='replace', index=False)
    #write tweet_table
    for index, row in df.iterrows():
        cursor.execute('''
            INSERT INTO data_table VALUES (?, ?, ?)
        ''', tuple(row))
    # cursor.executemany('''
    # INSERT INTO tweet_table (Tweet, Tweet_Cleaned) VALUES (?, ?)
    # ''', data)

    conn.commit()
    conn.close()

def create_text_db(dict):
    conn = sqlite3.connect('dataset\challenge_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS data_table (
        text TEXT,
        label TEXT,
        text_clean TEXT
    )
    ''')
    columns = ', '.join(dict.keys())
    placeholders = ', '.join(['?'] * len(dict))
    values = list(dict.values())

    query = f"INSERT INTO data_table ({columns}) VALUES ({placeholders})"
    cursor.execute(query, values)
    conn.commit()
    conn.close()