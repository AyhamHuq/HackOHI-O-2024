import sqlite3
import os
import sys
from collections import namedtuple
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../processing'))

from sql import sql

data = namedtuple('data', ['pk1', 'pk2', 'text'])

class fetcher:

    def filter_stop_words(text: str) -> str:
        lemmatizer = WordNetLemmatizer()

        # Initialize stop words
        stop_words = set(stopwords.words('english'))
        # Tokenize the text (split into words)
        tokens = text.split()
        # Remove stop words
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        filtered_tokens = [lemmatizer.lemmatize(word) for word in tokens]

        return ' '.join(filtered_tokens)


    def get_descriptions(cursor:sqlite3.Cursor) -> list[data]:
        l = []

        cursor.execute(sql.retrieve_sql)

        for row in cursor.fetchall():
            (
                observation_no, 
                point_name, 
                qualifier_text, 
                risk_notes, 
                risk_follow_up
            ) = row
            
            descriptiion = fetcher.filter_stop_words(' '.join([
                point_name, 
                qualifier_text, 
                risk_notes, 
                risk_follow_up or ''
            ]))

            l.append(data(observation_no, point_name, descriptiion))

        return l